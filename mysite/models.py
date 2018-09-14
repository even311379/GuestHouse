from django.db import models

# Create your models here.

class room_types(models.Model):
    name = models.CharField(max_length = 10,verbose_name = '房型')
    room_name = models.CharField(max_length = 10,verbose_name = '房間名稱')
    room_price = models.IntegerField(default = 3000, verbose_name = '平日價格')
    holiday_price = models.IntegerField(default = 3000, verbose_name = '假日價格')
    N_room = models.IntegerField(default = 4, verbose_name = '房間數')
    N_people = models.IntegerField(default = 2, verbose_name = '人數上限')

    def __str__(self):
        return self.name


class price_multifier(models.Model):
    multifier = models.DecimalField(max_digits = 3, decimal_places = 2, verbose_name = '折扣')
    sday = models.DateField(auto_now = False, verbose_name = '折扣開始日期')
    eday = models.DateField(auto_now = False, verbose_name = '折扣結束日期')

class holidays(models.Model):
    holiday_name = models.CharField(max_length = 10,verbose_name = '假日名稱', default='某國定假日')
    holiday_date = models.DateField(auto_now = False, verbose_name= '假日日期')

    # def __str__(self):
    #     return self.holiday_date

class FileUpload(models.Model):
    file = models.FileField(blank = True, verbose_name = '輔助檔案名稱')



class room_use_condition(models.Model):

    room_type_choice = (
    ('M1', 'Medium1'),
    ('M2', 'Medium2'),
    ('M3', 'Medium3'),
    ('M4', 'Medium4'),
    ('L1', 'Large1'),
    ('L2', 'Large2'),
    ('L3', 'Large3'),
    ('L4', 'Large4'),
    ('L5', 'Large5'),
    ('L6', 'Large6'),
    ('G1','Group1'),
    ('G2','Group2'),
    ('G3','Group3'),
    )

    # 中的4間 6大的間 都是4人房
    
    room_type = models.CharField(max_length = 2, choices = room_type_choice, verbose_name = '房型')
    room_start_use_date = models.DateField(auto_now = False, verbose_name = '開始使用日期')
    room_end_use_date = models.DateField(auto_now = False, verbose_name = '結束使用日期')
    confirmed = models.BooleanField(default = False, verbose_name = '已確認？')

    booker_name = models.CharField(max_length = 25, verbose_name = '訂房人姓名')
    booking_time = models.DateTimeField(auto_now = False, verbose_name = '訂房時間')
    booker_phone = models.CharField(max_length = 20, verbose_name = '訂房人電話號碼')
    booker_email = models.EmailField(max_length = 30, verbose_name = '訂房人電子信箱')
    confirmed_time = models.DateTimeField(auto_now = False, verbose_name = '確認時間')

    '''
    Severe issue found!!
    blank = True seems will cause severe problem when I want create one date through code...
    '''


