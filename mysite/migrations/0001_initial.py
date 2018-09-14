# Generated by Django 2.1.1 on 2018-09-13 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to='', verbose_name='輔助檔案名稱')),
            ],
        ),
        migrations.CreateModel(
            name='holidays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('holiday_name', models.CharField(default='某國定假日', max_length=10, verbose_name='假日名稱')),
                ('holiday_date', models.DateField(verbose_name='假日日期')),
            ],
        ),
        migrations.CreateModel(
            name='price_multifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('multifier', models.DecimalField(decimal_places=2, max_digits=3, verbose_name='折扣')),
                ('sday', models.DateField(verbose_name='折扣開始日期')),
                ('eday', models.DateField(verbose_name='折扣結束日期')),
            ],
        ),
        migrations.CreateModel(
            name='room_types',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='房型')),
                ('room_name', models.CharField(max_length=10, verbose_name='房間名稱')),
                ('room_price', models.IntegerField(default=3000, verbose_name='平日價格')),
                ('holiday_price', models.IntegerField(default=3000, verbose_name='假日價格')),
                ('N_room', models.IntegerField(default=4, verbose_name='房間數')),
                ('N_people', models.IntegerField(default=2, verbose_name='人數上限')),
            ],
        ),
        migrations.CreateModel(
            name='room_use_condition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_type', models.CharField(choices=[('M1', 'Medium1'), ('M2', 'Medium2'), ('M3', 'Medium3'), ('M4', 'Medium4'), ('L1', 'Large1'), ('L2', 'Large2'), ('L3', 'Large3'), ('L4', 'Large4'), ('L5', 'Large5'), ('L6', 'Large6'), ('G1', 'Group1'), ('G2', 'Group2'), ('G3', 'Group3')], max_length=2, verbose_name='房型')),
                ('room_start_use_date', models.DateField(verbose_name='開始使用日期')),
                ('room_end_use_date', models.DateField(verbose_name='結束使用日期')),
                ('confirmed', models.BooleanField(default=False, verbose_name='已確認？')),
                ('booker_name', models.CharField(blank=True, max_length=25, verbose_name='訂房人姓名')),
                ('booking_time', models.DateTimeField(blank=True, verbose_name='訂房時間')),
                ('booker_phone', models.CharField(blank=True, max_length=20, verbose_name='訂房人電話號碼')),
                ('booker_email', models.EmailField(blank=True, max_length=254, verbose_name='訂房人電子信箱')),
                ('confirmed_time', models.DateTimeField(blank=True, default=False, verbose_name='確認時間')),
            ],
        ),
    ]
