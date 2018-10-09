# -*- coding: utf-8 -*-
from mysite import models
import datetime
from collections import namedtuple
import os


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
            latest_start = max(r1.start, r2.sread_holiday_csvtart)
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


def load_logos():
    pass


if __name__ == '__main__':
    a, b = read_holiday_csv()
    print(a[:5], b[:5])
    print(a[-5:], b[-5:])
