"""简单的创建测试环境的脚本"""
import sys
import os
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model


pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"/../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DinDonBackend.settings")

import django
django.setup()

from Tables.models import Table
from Dishes.models import Dish

User = get_user_model()

class InitDB:
    def init_user(self):
        u1 = User.objects.update_or_create(
            username='custom1',
            password=make_password('admin123'),
            user_type=0)

    def init_table(self):
        tb1 = Table.objects.update_or_create()

    def init_dish(self):
        d1 = Dish.objects.update_or_create(dish_name='菜品1',
                                           dish_price=10,
                                           )
        d2 = Dish.objects.update_or_create(
                                            dish_name='菜品2',
                                            dish_price=20,
                                            )

    def main(self):
        self.init_user()
        self.init_dish()
        self.init_table()
        print('create db success')

if __name__ == '__main__':
    InitDB().main()