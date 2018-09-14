from mysite import models
import datetime
from collections import namedtuple

def check_free_rooms(sd, eud):
	rooms_data = models.room_use_condition.objects.filter(room_end_use_date__gte = datetime.date.today())

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
			if (earliest_end - latest_start).days >= 0:
				break
		else:
			empty_rooms.append(rt)

	return empty_rooms

'''
換房間問題

'''