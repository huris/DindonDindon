from alipay import AliPay
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from DinDonBackend.permissions import UserBasePermission, SuperPermission, CustomerPermission
from Orders.models import Order, Transaction, OrderStatus
from Orders.serializers import OrderSerializer, TransactionSerializer, TransactionUpdateSerializer
from Users.models import UserType
# from Utils.keys.Key import AliPayKey
from Utils.keys.Key_example import AliPayKey

class OrderListView(ListAPIView):
    """
    当前用户订单列表
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (UserBasePermission,)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.user_type == UserType.Manager:
            return Order.objects.all()
        else:
            return Order.objects.filter(order_user=user)


class OrderRetrieveAPIView(RetrieveAPIView):
    """
    取回订单
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (SuperPermission | CustomerPermission,)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.user_type == UserType.Manager:
            return Order.objects.all()
        else:
            return Order.objects.filter(order_user=user)


class OrderCreateView(CreateAPIView):
    """
    创建订单并生成支付链接
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (CustomerPermission,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        price = serializer.validated_data['order_price']

        Host = "xxxxx:8000"
        # ret_url = "http://" + Host + "/orders/notify"
        """
        我的建议是notify_url和return_url不应该是一致的，
        notify_url接口的作用是获取支付宝返回的订单信息，存入数据库，
        return_url接口是展示某个已经付完款订单的详细信息(当然也可以换成其他的，根据自己的设计，付完款后跳到哪里去)
        """
        ret_url = "http://" + Host + "/orders/{pk}".format(pk=instance.order_id)
        notify_url = "http://" + Host + "/orders/notify"

        app_private_key = AliPayKey.app_private_key()
        alipay_public_key = AliPayKey.alipay_public_key()
        alipay = AliPay(
            appid=AliPayKey.APP_ID,
            app_notify_url=notify_url,  # 默认回调url
            app_private_key_string=app_private_key,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False
        )
        order_id = serializer.data['order_id']
        order_id = str(order_id)
        order_string = alipay.api_alipay_trade_wap_pay(
            out_trade_no=order_id,
            total_amount=price,
            subject="支付订单",
            return_url=ret_url,
            # notify_url=ret_url  # 可选, 不填则使用默认notify url
        )

        pay_url = AliPayKey.GATEWAY_DEV + "?" + order_string

        ret_data = {
            "pay_url": pay_url
        }

        ret_data.update(serializer.data)

        return Response(ret_data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

class AlipayProcessView(APIView):
    # def get(self, request, *args, **kwargs):
    #     pass

    def post(self, request):
        print('callback ok')

        # TODO 在这里拿到订单号，先进行签名验证，确保这个跳转是从支付宝过来的，
        #  然后拿到订单状态等一些信息，存入数据库

        # NOTE： 一定要返回"success",不能是别的信息
        return Response('success')


class OrderProcessView(UpdateAPIView):
    """
    订单处理
    """
    permission_classes = (UserBasePermission,)
    lookup_field = 'order'
    queryset = Transaction.objects.all()
    serializer_class = TransactionUpdateSerializer
