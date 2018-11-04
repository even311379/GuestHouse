from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from mysite import models
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils import timezone
from django.contrib import messages
from mysite.utils import check_free_rooms, read_holiday_csv, slack_message, remove_unconfirmed_bookings, check_send_email_failure

import datetime
import calendar

# Create your views here.

EMAIL_SERVER = 'even311379@gmail.com'
HOST_USER_EMAILS = ['even311379@hotmail.com', 'cth30@outlook.com']


def home(request):
    return HttpResponse(render(request, '../templates/home.html', locals()))


def news(request):
    news = True
    all_news = models.news_dashboard.objects.all()
    
    # print(request.user_agent.is_mobile)
    # print(request.user_agent.browser)
    return HttpResponse(render(request, '../templates/news.html', locals()))


def about(request):
    about = True
    return HttpResponse(render(request, '../templates/about.html', locals()))


def roomtype(request):
    roomtype = True
    return HttpResponse(render(request, '../templates/roomtype.html', locals()))


def booking(request):
    booking = True

    # default inday and outday are today and tomorrow
    str_inday = datetime.date.today().strftime("%Y-%m-%d")
    str_outday = (datetime.date.today() +
                  datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    try:
        form_id = request.GET.get('Form id')
    except:
        pass

    # 處理第一個表單的變數
    if request.method == 'GET' and form_id == '0':

        sd = request.GET.get('room_start_date')
        ed = request.GET.get('room_end_date')
        sd = datetime.datetime.strptime(sd, '%Y-%m-%d').date()
        ed = datetime.datetime.strptime(ed, '%Y-%m-%d').date()
        str_inday = sd.strftime("%Y-%m-%d")
        str_outday = ed.strftime("%Y-%m-%d")
        eud = ed - datetime.timedelta(days=1)  # end use date
        n_night = (ed-sd).days

        daylist = []
        d = sd
        while d < ed:
            daylist.append(d)
            d += datetime.timedelta(days=1)

        n_holiday = 0
        _, all_holidays = read_holiday_csv()
        # 隔天假日，前一晚就以假日計費
        all_holidays = [d - datetime.timedelta(days=1) for d in all_holidays]
        for date in daylist:
            if date in all_holidays:
                n_holiday += 1

        if n_night <= 0:
            messages.add_message(request, messages.WARNING, "退房日期輸入錯誤")
            messages.get_messages(request)
            return HttpResponseRedirect('booking')

        # Check free room logic here:
        empty_rooms = check_free_rooms(sd, eud)

        ED = dict(L=0, M=0, G=0)
        for i in empty_rooms:
            for rt in ['L', 'M', 'G']:
                if i.startswith(rt):
                    ED[rt] += 1
        RT = []
        N_room_left = []

        for k in ED:
            if ED[k] > 0:
                RT.append(k)
                N_room_left.append(ED[k])

        remove_unconfirmed_bookings()
        empty_room_types = [models.room_types.objects.filter(name=t)[
            0] for t in RT]
        N_room_range = [list(range(1, n+1)) for n in N_room_left]
        empty_room_info = zip(empty_room_types, N_room_left, N_room_range)

    # 處理第二個表單的變數
    if request.method == 'POST' and request.POST.get('Form id') == '1':
        types = []
        N_booking = []
        sd = request.POST['room_start_date']
        eud = request.POST['room_end_date']
        for t in ['年', '月']:
            sd = sd.replace(t, '-')
            eud = eud.replace(t, '-')

        ed = datetime.datetime.strptime(
            eud[:-1], '%Y-%m-%d').date()+datetime.timedelta(days=1)
        ed = ed.strftime("%Y-%m-%d")
        for key in request.POST:
            if key.startswith('N'):
                types.append(key[2:])
                N_booking.append(int(request.POST[key]))

        if sum(N_booking) == 0:
            messages.add_message(request, messages.WARNING, "請至少輸入一間房間")
            messages.get_messages(request)
            form_id = '0'
            return HttpResponseRedirect('booking?room_start_date={0}&room_end_date={1}&Form+id=0'.format(sd[:-1], ed))

        else:
            '''
            pack data via sessions and go to booking_check
            '''
            daylist = []
            d = datetime.datetime.strptime(sd[:-1], '%Y-%m-%d').date()
            while d <= datetime.datetime.strptime(eud[:-1], '%Y-%m-%d').date():
                daylist.append(d)
                d += datetime.timedelta(days=1)
            request.session['booking_order_info'] = str(
                dict(BT=types, NB=N_booking, DL=daylist))

            return HttpResponseRedirect('booking_check')

    return HttpResponse(render(request, '../templates/booking.html', locals()))

def booking_validate_date(request):
    '''
    This is a ajax response
    '''
    end_date = request.GET.get('end_date', None)
    start_date = request.GET.get('start_date', None)
    data = {
        'problematic': datetime.datetime.strptime(start_date, '%Y-%m-%d') >= datetime.datetime.strptime(end_date, '%Y-%m-%d')
    }
    return JsonResponse(data)


def booking_check(request):
    try:
        book_order_info = eval(request.session.get('booking_order_info'))
    except:
        # if no session data, redirect back to booking
        return HttpResponseRedirect('booking')

    n_holiday = 0
    _, all_holidays = read_holiday_csv()
    all_holidays = [d - datetime.timedelta(days=1)
                    for d in all_holidays]  # 隔天假日，前一晚就以假日計費
    for date in book_order_info['DL']:
        if date in all_holidays:
            n_holiday += 1

    n_workday = len(book_order_info['DL']) - n_holiday
    check_in = book_order_info['DL'][0]
    check_out = book_order_info['DL'][-1] + datetime.timedelta(days=1)

    nb_shown = []
    bt_shown = []
    bt_dbname = []
    money_shown = []
    for bt, nb in zip(book_order_info['BT'], book_order_info['NB']):
        if nb > 0:
            rt = models.room_types.objects.filter(name=bt)[0]
            nb_shown += [nb]
            bt_shown += [rt.room_name]
            bt_dbname.append(rt.name)
            money_shown += [rt.room_price * nb *
                            n_workday + rt.holiday_price * nb * n_holiday]

    order_info = zip(bt_shown, nb_shown, money_shown)
    total_sum = sum(money_shown)
    request.session['booking_order_info_confirmed'] = str(dict(rt=bt_shown, nb=nb_shown, bt=bt_dbname, money=money_shown,
                                                               nd=n_workday, nhd=n_holiday, check_in=check_in, check_out=check_out))
    request.session.pop('booking_order_info')
    return HttpResponse(render(request, '../templates/booking_check.html', locals()))


def add_booking_data(request):
    booking = True
    if request.method == 'POST':
        try:
            BookerName = request.POST.get('BookerName')
            BookerEmail = request.POST.get('BookerEmail')
            BookerPhone = request.POST.get('BookerPhone')
            boic = eval(request.session.get('booking_order_info_confirmed'))
            order_info = zip(boic['rt'], boic['nb'], boic['money'])
            total = sum(boic['money'])
            nd, nhd, check_in, check_out = boic['nd'], boic['nhd'], boic['check_in'], boic['check_out']
            eud = check_out - datetime.timedelta(days=1)

            # assign empty rooms for booking
            rts = []
            free_rooms = check_free_rooms(check_in, eud)

            for r, n in zip(boic['bt'], boic['nb']):
                a = 0
                while a < n:
                    r_picked = [fr for fr in free_rooms if fr.startswith(r)][0]
                    rts.append(r_picked)
                    free_rooms.remove(r_picked)
                    a += 1

            # try:
            ruc_id = []
            for rt in rts:
                new_room_use_condition = models.room_use_condition.objects.create(room_type=rt, room_start_use_date=check_in,
                                                                                  room_end_use_date=eud, booker_name=BookerName, booking_time=timezone.now(),
                                                                                  booker_phone=BookerPhone, booker_email=BookerEmail, confirmed_time=timezone.now(), confirmed=False)
                new_room_use_condition.save()
                ruc_id.append(new_room_use_condition.id)
            '''
            寄email給客人
            '''
            mail_template = get_template('book_email.html')
            confirmed_date = datetime.date.today() + datetime.timedelta(days=3)
            content = mail_template.render(locals())
            subject = '感謝您預定湖頂麒麟潭農場民宿'
            msg = EmailMessage(
                subject, content, EMAIL_SERVER, [BookerEmail])
            msg.content_subtype = 'html'

            try:
                msg.send()
            except Exception as e:
                print('Send mail fail!')
                print(e)


            '''
            發送通知(slack)，提醒去查看email確認訂單。
            '''
            slack_message('{}向您訂房囉！快打開信箱確認訂單吧！'.format(BookerName))

            '''
            寄mail給民宿業者，在此mail中確認此訂單
            '''
            mail_template = get_template('book_confirm_email.html')
            content = mail_template.render(locals())
            subject = '民宿網站訂房通知'
            msg = EmailMessage(
                subject, content, EMAIL_SERVER, HOST_USER_EMAILS)
            msg.content_subtype = 'html'
            request.session.pop('booking_order_info_confirmed')

            try:
                msg.send()
                # 'cth30@outlook.com'
            except Exception as e:
                print('Send mail fail!')
                print(e)

        except Exception as e:
            print('Unexpected Errows!!')
            print(e)

    return HttpResponseRedirect('/')


def booking_data_confirm(request):
    booking = True
    if request.method == 'GET':

        for key in request.GET:
            ids = eval(request.GET[key])
        rcs_to_confirm = models.room_use_condition.objects.filter(pk__in=ids)
        '''
        Add email confirm function here
        if the bookering email is correct, do it, redirect to a success page
        else, don't do it, and redirect to a fail page which contains the booker's phone number 
        '''

        # 時區要設一樣，所以變為gmt0，要+8 回來
        ctime = (rcs_to_confirm[0].booking_time + datetime.timedelta(hours=8)).replace(tzinfo=None)

        if check_send_email_failure(ctime):
            request.session['fail_phone_numer'] = str(rcs_to_confirm[0].booker_phone)
            return HttpResponseRedirect('/booking_fail')

        for rc in rcs_to_confirm:
            rc.confirmed = True
            rc.confirmed_time = timezone.now()
            rc.save()
        print('Great! Successfully confirming the bookings')

        buser = rcs_to_confirm[0].booker_name
        bemail = rcs_to_confirm[0].booker_email
        mail_template = get_template('book_success_email.html')
        content = mail_template.render(locals())
        subject = 'xx民宿訂房成功'
        msg = EmailMessage(subject, content, EMAIL_SERVER, [bemail, ])
        msg.content_subtype = 'html'
        try:
            msg.send()
        except Exception as e:
            print(e)

    '''
	Should I redirect to a better html in order to make the host_user know that this step is done?

    Yes! I should!
	'''
    return HttpResponseRedirect('/booking_success')

def booking_success(request):
    return HttpResponse('<h1>success</h1>')

def booking_fail(request):
    phone = request.session.get('fail_phone_numer')
    request.session.pop('fail_phone_numer')
    '''
    然後殺掉這筆訂單嗎？
    '''
    return HttpResponse('<h1>fail</h1><h2>{}</h2>'.format(phone))

def traffic(request):
    traffic = True
    return HttpResponse(render(request, '../templates/traffic.html', locals()))


def nearby(request):
    nearby = True
    all_nearby = models.nearby_dashboard.objects.all()
    return HttpResponse(render(request, '../templates/nearby.html', locals()))


def calendar_widget(request):

    room_left = True
    remove_unconfirmed_bookings()
    if request.method == 'POST':
        Y = int(request.POST.get('Year'))
        M = int(request.POST.get('Month'))
    else:
        Y = datetime.date.today().year
        M = datetime.date.today().month

    N_days = calendar.monthrange(Y, M)[1]
    first_date = datetime.date(Y, M, 1)
    dates = []
    weekdays = []

    for i in range(N_days):
        dates.append(first_date+datetime.timedelta(days=i))
        weekdays.append((first_date+datetime.timedelta(days=i)).weekday())

    if first_date.weekday() != 6:
        head_append = list(range(first_date.weekday()+1))
    else:
        head_append = []
    tail_append = list(range(5 - dates[-1].weekday()))
    all_booking_data = models.room_use_condition.objects.all()
    booking_data_this_month = []
    for data in all_booking_data:
        if data.room_start_use_date.month == M or data.room_end_use_date.month == M:
            booking_data_this_month.append(data)

    # loop every date in this month to pack special date and booking date for template to render
    booking_this_month = []
    all_holidays_comment, all_holidays = read_holiday_csv()
    # all_holidays = [d - datetime.timedelta(days=1) for d in all_holidays]
    holiday_bool = []
    holiday_comment = []
    for date in dates:
        booking_this_day = []
        for booking_data in booking_data_this_month:
            if booking_data.room_start_use_date <= date <= booking_data.room_end_use_date:
                booking_this_day.append(booking_data.room_type)
        nL, nM, nG = [
            len([i for i in booking_this_day if i.startswith(T)]) for T in 'LMG']
        booking_this_month.append(
            "四人大套房: {0}<br>三人套房: {1}<br>和式團體房: {2}".format(6-nL, 4-nM, 3-nG))

        if date in all_holidays:
            holiday_bool.append(True)
            holiday_comment.append(
                all_holidays_comment[all_holidays.index(date)])
        else:
            holiday_bool.append(False)
            holiday_comment.append('')

    dateinfo = zip(dates, weekdays, booking_this_month,
                   holiday_bool, holiday_comment)
    return HttpResponse(render(request, '../templates/calendar_widget.html', locals()))


def message_area(request):
    message_area = True
    all_guest_messages = models.guest_message.objects.all().order_by('-ask_time')
    paginator = Paginator(all_guest_messages, 10)
    p = request.GET.get('p')
    if not p:
        p = 1
    try:
        guest_messages = paginator.page(p)
        print(guest_messages[0].message)
    except PageNotAnInteger:
        guest_messages = paginator.page(1)
    except EmptyPage:
        guest_messages = paginator.page(paginator.num_pages())

    return HttpResponse(render(request, '../templates/message_area.html', locals()))


def add_message(request):
    if request.method == 'POST':
        who = request.POST.get('who')
        what = request.POST.get('what').replace('\n', '<br>')
        secret = request.POST.get('SecretCheck1')

        if secret:
            # print('Add send Email logic later')
            email = request.POST.get('Email')
            mail_template = get_template('secret_message_email.html')
            content = mail_template.render(locals())
            subject = '民宿網站悄悄話'
            msg = EmailMessage(
                subject, content, EMAIL_SERVER, HOST_USER_EMAILS)
            msg.content_subtype = 'html'
            try:
                msg.send()
            except Exception as e:
                print(e)

        else:
            new_message = models.guest_message.objects.create(
                guest_name=who, message=what, ask_time=datetime.datetime.now())
            new_message.save()

    else:
        pass

    return HttpResponseRedirect('message_area')
