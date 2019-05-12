# Generated by Django 2.2.1 on 2019-05-12 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('announcementId', models.AutoField(primary_key=True, serialize=False, verbose_name='公告编号')),
                ('announcementContent', models.TextField(null=True, verbose_name='公告内容')),
                ('announcementPublishTime', models.DateTimeField(auto_now_add=True, verbose_name='公告发布时间')),
                ('announcementModifyTime', models.DateTimeField(auto_now=True, verbose_name='公告修改时间')),
            ],
            options={
                'verbose_name': '公告',
                'verbose_name_plural': '公告',
            },
        ),
    ]
