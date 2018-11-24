from django.db import models

# Create your models here.


class room_types(models.Model):
    class Meta: # set the class name shown in admin
        verbose_name = '房型基本資料'
        verbose_name_plural = '房型基本資料'

    name = models.CharField(max_length=10, verbose_name='房型')
    room_name = models.CharField(max_length=10, verbose_name='房間名稱')
    room_price = models.IntegerField(default=3000, verbose_name='平日價格')
    holiday_price = models.IntegerField(default=3000, verbose_name='假日價格')
    N_room = models.IntegerField(default=4, verbose_name='房間數')
    N_people = models.IntegerField(default=2, verbose_name='人數上限')

    def __str__(self):
        return self.name


class price_multifier(models.Model): # No function for this stuff so far
    class Meta: 
        verbose_name = '打折設定'
        verbose_name_plural = '打折設定'

    multifier = models.DecimalField(
        max_digits=3, decimal_places=2, verbose_name='折扣')
    sday = models.DateField(auto_now=False, verbose_name='折扣開始日期')
    eday = models.DateField(auto_now=False, verbose_name='折扣結束日期')


class FileUpload(models.Model):
    class Meta: 
        verbose_name = '上傳輔助檔案'
        verbose_name_plural = '上傳輔助檔案'
    file = models.FileField(blank=True, verbose_name='輔助檔案名稱')


class room_use_condition(models.Model):
    class Meta:
        verbose_name = '用房狀況'
        verbose_name_plural = '用房狀況'

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
        ('G1', 'Group1'),
        ('G2', 'Group2'),
        ('G3', 'Group3'),
    )

    # 中的4間 6大的間 都是4人房

    room_type = models.CharField(
        max_length=2, choices=room_type_choice, verbose_name='房型')
    room_start_use_date = models.DateField(
        auto_now=False, verbose_name='開始使用日期')
    room_end_use_date = models.DateField(auto_now=False, verbose_name='結束使用日期')
    confirmed = models.BooleanField(default=False, verbose_name='已確認？')

    booker_name = models.CharField(max_length=25, verbose_name='訂房人姓名')
    booking_time = models.DateTimeField(auto_now=False, verbose_name='訂房時間')
    booker_phone = models.CharField(max_length=20, verbose_name='訂房人電話號碼')
    booker_email = models.EmailField(max_length=30, verbose_name='訂房人電子信箱')
    confirmed_time = models.DateTimeField(auto_now=False, verbose_name='確認時間')

    '''
    Severe issue found!!
    blank = True seems will cause severe problem when I want create one date through code...
    '''


class guest_message(models.Model):
    class Meta:
        verbose_name = '顧客留言'
        verbose_name_plural = '顧客留言'

    guest_name = models.CharField(max_length=15, verbose_name='誰')
    message = models.TextField(verbose_name='說啥')
    ask_time = models.DateTimeField(auto_now=False, verbose_name='詢問時間')
    has_replied = models.BooleanField(default=False, verbose_name='已回覆？')
    replied_message = models.TextField(default='感謝您！', verbose_name='回覆啥')
    replied_time = models.DateTimeField(auto_now=True, verbose_name='回覆時間')


class news_dashboard(models.Model):
    class Meta:
        verbose_name = '最新消息'
        verbose_name_plural = '最新消息'

    news_title = models.CharField(max_length=30, verbose_name='標題')
    news_content = models.TextField(verbose_name='內容')
    news_thumbnail = models.FileField(verbose_name='縮圖')
    news_upload_time = models.DateTimeField(auto_now=True, verbose_name='發布時間')

class nearby_dashboard(models.Model):
    class Meta:
        verbose_name = '附近景點'
        verbose_name_plural = '附近景點'

    nearby_title = models.CharField(max_length=30, verbose_name='標題')
    nearby_content = models.TextField(verbose_name='內容')
    nearby_thumbnail = models.FileField(verbose_name='縮圖')
    nearby_upload_time = models.DateTimeField(auto_now=True, verbose_name='發布時間')