# Generated by Django 2.2.1 on 2019-05-11 10:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Orders', '0002_order_ordertable'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='orderUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='订单用户'),
        ),
    ]