# -*- coding: utf-8 -*-
from mysite import models
import datetime
from collections import namedtuple
from slackclient import SlackClient
import os
import MyImportantInfo as MIF
import imaplib
import email

def check_free_rooms(sd, eud):
    rooms_data = models.room_use_condition.objects.filter(
        room_end_use_date__gte=datetime.date.today())

    Range = namedtuple('Range', ['start', 'end'])
    all_room_types = ['M1', 'M2', 'M3', 'M4', 'L1', 'L2', 'L3', 'L4',
                      'L5', 'L6', 'G1', 'G2', 'G3']
    empty_rooms = []
    r1 = Range(start=sd, end=eud)
    for rt in all_room_types:
        candidate_rooms = rooms_data.filter(room_type=rt)
        for r in candidate_rooms:
            r2 = Range(start=r.room_start_use_date, end=r.room_end_use_date)
            latest_start = max(r1.start, r2.start)
            earliest_end = min(r1.end, r2.end)
            if (earliest_end - latest_start).days >= 0:
                break
        else:
            empty_rooms.append(rt)

    return empty_rooms


'''
換房間問題

'''


def read_holiday_csv():

    holiday_comment = []
    holiday_date = []
    files = ['media/'+f for f in os.listdir('media/') if 'holidays.csv' in f]
    print(files)
    for file in files:
        try:
            with open(file) as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(file, encoding='big5') as f:
                content = f.read()
        except Exception as e:
            print('!! Unkonw error: {}'.format(e))

        for row in content.split('\n')[1:]:
            try:
                if row.split(',')[2] == '2':
                    d = row.split(',')[0]
                    holiday_date.append(datetime.date(int(d[0:4]), int(d[4:6]), int(d[6:8])))
                    holiday_comment.append(row.split(',')[3])
            except Exception as e:
                # print(e)
                pass
    return holiday_comment, holiday_date


'''
SmartPhone notification through slack
'''


def slack_message(message, channel='訂房通知'):
    token = MIF.slack_api_key()
    sc = SlackClient(token)

    sc.api_call('chat.postMessage', channel=channel,
                text=message, username='機器人',
                icon_emoji=':robot_face:')


def remove_unconfirmed_bookings():
    rooms_data = models.room_use_condition.objects.filter(
        confirmed=False)
    for data in rooms_data:
        if datetime.date.today() - data.booking_time.date() > datetime.timedelta(days=3):
            print('One row is deleted!')
            data.delete()


def check_send_email_failure(booking_datetime):
    '''
    去郵件伺服器內檢視所有信件是否有計件失敗的信件
    (from ==  Mail Delivery Subsystem <mailer-daemon@googlemail.com>)
    若有，將收信的時間拿出來，再和訂房人訂房時間booking_datetime比對，如果時間差(5分鐘)？內，
    即判定訂房人當初的信箱填錯，而導致寄信失敗，return True
    '''

    M = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    M.login(MIF.MyGmailAccount().split('@')[0], MIF.MyGmailPassword())

    # M.list() # Lists all labels in GMail
    M.select('inbox') # Connected to inbox.
    __, ids = M.uid('search', None, "ALL")

    Failure_datetime = []
    for uid in str(ids[0])[2:-1].split(' '):
        try:
            __, email_data = M.uid('fetch', str(uid), 'RFC822')
            # fetch the email body (RFC822) for the given ID
            msg = email.message_from_bytes(email_data[0][1])
            if msg['from'] == 'Mail Delivery Subsystem <mailer-daemon@googlemail.com>':
                u_failtime = datetime.datetime.strptime(msg['date'].split(',')[1][1:21], "%d %b %Y %H:%M:%S")
                u_failtime = u_failtime.replace(tzinfo=None)
                Failure_datetime.append(u_failtime + datetime.timedelta(hours=15))
                '''
                網域的時區為gmt+8 而mailer-daemon@googlemail.com的時間為PDT( = gmt-7)
                所以統一時間要加15小時 
                '''
        except Exception as e:
            print(e)
    M.close()
    M.logout()

    print(booking_datetime)
    print('\n')
    if not Failure_datetime:
        return False
    for fdt in Failure_datetime:
        print(fdt)
        if abs((fdt - booking_datetime).total_seconds()) <= 300:
            return True
    else:
        return False

if __name__ == '__main__':
    a, b = read_holiday_csv()
    print(a[:5], b[:5])
    print(a[-5:], b[-5:])