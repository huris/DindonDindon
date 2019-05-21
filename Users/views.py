import random
from django.contrib.auth.hashers import make_password

from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from DinDonBackend.permissions import UserBasePermission
from Users.models import VerifyCode, User
from Users.serializers import SmsCodeSerializer, LoginWithSmsCodeSerializer, UserRegisterSerializer, \
    UserChangePasswordSerializer


class SmsCodeView(CreateAPIView):
    """
    获取短信验证码
    """
    queryset = VerifyCode.objects.all()
    serializer_class = SmsCodeSerializer

    def post(self, request, *args, **kwargs):
        purpose = request.data.get('purpose', 0)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']

        # 生成6位随机验证码
        code = "%06d" % random.randint(0000, 9999)
        # 调试使用
        code = "123456"
        # TODO 调用第三方发送短信验证码的接口

        try:
            VerifyCode.objects.create(phone_number=phone_number,
                                      code=code,
                                      purpose=purpose
                                      )
            return Response({"status": "发送成功"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"status": "发送失败"}, status=status.HTTP_400_BAD_REQUEST)


class LoginWithSmsCodeView(CreateAPIView):
    """
    使用短信验证码登录
    """
    queryset = User.objects.all()
    serializer_class = LoginWithSmsCodeSerializer
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        user = User.objects.filter(phone_number=phone_number).first()

        token = TokenObtainPairSerializer().get_token(user)
        data = serializer.data
        data.update({'uid': user.id})
        data.update({'username': user.username})
        data.update({'refresh': str(token)})
        data.update({'access': str(token.access_token)})

        return Response(data, status=status.HTTP_200_OK)


class UserRegisterView(CreateAPIView):
    """
    用户注册
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        data = serializer.data
        token = TokenObtainPairSerializer().get_token(user)
        data.update({'uid': user.id})
        data.update({'username': user.username})
        data.update({'refresh': str(token)})
        data.update({'access': str(token.access_token)})

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save(password=make_password(serializer.validated_data['password']))


class UserChangePasswordView(UpdateAPIView):
    serializer_class = UserChangePasswordSerializer
    permission_classes = (UserBasePermission,)

    def get_queryset(self):
        return User.objects.filter(phone_number=self.request.user.phone_number)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({'message': '密码修改成功'}, status=status.HTTP_200_OK)
