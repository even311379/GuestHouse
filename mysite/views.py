from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from mysite import models
from django.contrib import messages, auth
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
import datetime
from collections import namedtuple
# Create your views here.

def home(request):
	return HttpResponse(render(request, '../templates/home.html', locals()))

def news(request):
	return HttpResponse(render(request, '../templates/news.html', locals()))

def about(request):
	return HttpResponse(render(request, '../templates/about.html', locals()))

def roomtype(request):
	return HttpResponse(render(request, '../templates/roomtype.html', locals()))

def booking(request):

	# default inday and outday are today and tomorrow
	str_inday = datetime.date.today().strftime("%Y-%m-%d")
	str_outday = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

	if request.method=='POST':

		sd = request.POST.get('room_start_date')
		ed = request.POST.get('room_end_date')
		sd = datetime.datetime.strptime(sd, '%Y-%m-%d').date()
		ed = datetime.datetime.strptime(ed, '%Y-%m-%d').date()
		str_inday = sd.strftime("%Y-%m-%d")
		str_outday = ed.strftime("%Y-%m-%d")
		eud = ed - datetime.timedelta(days = 1) # end use date
		n_night = (ed-sd).days

		# Check free room logic here:
		rooms_data = models.room_use_condition.objects.filter(
			room_end_use_date__gte= datetime.date.today() - datetime.timedelta(days=1))

		Range = namedtuple('Range', ['start', 'end'])
		all_room_types = ['M1', 'M2', 'M3', 'M4','L1', 'L2','L3', 'L4',
		'L5', 'L6', 'G1', 'G2', 'G3']
		empty_rooms = []
		r1 = Range(start=sd, end=eud)
		for rt in all_room_types:
			candidate_rooms = rooms_data.filter(room_type = rt)
			for r in candidate_rooms:
				r2 = Range(start = r.room_start_use_date, end = r.room_end_use_date)
				latest_start = max(r1.start, r2.start)
				earliest_end = min(r1.end, r2.end)
				if (earliest_end - latest_start).days > 0:
					break
			else:
				empty_rooms.append(rt)

		types = set([i[0] for i in empty_rooms])
		empty_room_types = models.room_types.objects.filter(name__in=types)

		N_room_left = [sum([i[0]==L for i in empty_rooms]) for L in ['M','L','G']]
		N_room_range = [list(range(1,n+1)) for n in N_room_left]

		empty_room_info = zip(empty_room_types, N_room_left, N_room_range)




		# rooms = [r for r in all_rooms if r not in [r.room_type for r in  used_rooms]]
		# rooms = [r.room_type for r in  used_rooms]

		# 新增房間使用狀況時, room_end_use_date = 退房日期 - timedelta(days=1)

	return HttpResponse(render(request, '../templates/booking.html', locals()))

def booking_check(request):
	if request.method=='POST':
		for key in request.POST:
		    print(key)
		    value = request.POST[key]
		    print(value)
		return HttpResponse(render(request, '../templates/booking_check.html', locals()))
	else:
		return redirect('home')

def book_confirm(request):
	return HttpResponse(render(request, '../templates/traffic.html', locals()))

def traffic(request):
	return HttpResponse(render(request, '../templates/traffic.html', locals()))

def nearby(request):
	return HttpResponse(render(request, '../templates/nearby.html', locals()))
