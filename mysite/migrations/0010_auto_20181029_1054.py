# Generated by Django 2.1.2 on 2018-10-29 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0009_news_dashboard'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nearby_dashboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nearby_title', models.CharField(max_length=30, verbose_name='標題')),
                ('Nearby_content', models.TextField(verbose_name='內容')),
                ('Nearby_thumbnail', models.FileField(upload_to='', verbose_name='縮圖')),
                ('Nearby_upload_time', models.DateTimeField(auto_now=True, verbose_name='發布時間')),
            ],
            options={
                'verbose_name': '附近景點',
            },
        ),
        migrations.DeleteModel(
            name='holidays',
        ),
        migrations.AlterModelOptions(
            name='guest_message',
            options={'verbose_name': '顧客留言'},
        ),
        migrations.AlterModelOptions(
            name='news_dashboard',
            options={'verbose_name': '最新消息'},
        ),
        migrations.AlterModelOptions(
            name='room_types',
            options={'verbose_name': '房型基本資料'},
        ),
        migrations.AlterModelOptions(
            name='room_use_condition',
            options={'verbose_name': '用房狀況'},
        ),
        migrations.AlterField(
            model_name='news_dashboard',
            name='news_upload_time',
            field=models.DateTimeField(auto_now=True, verbose_name='發布時間'),
        ),
    ]
