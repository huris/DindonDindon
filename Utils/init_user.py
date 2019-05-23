from Users.models import User

user = User(
    username="masterchef",
    user_type=2,
    is_staff=True,
    is_active=True
)
user.set_password("123456")
user.save()

user = User(
    username="masterwaiter",
    user_type=3,
    is_staff=True,
    is_active=True
)
user.set_password("123456")
user.save()