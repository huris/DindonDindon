class SMSAPIKey:
    AccessKey_ID = ""
    AccessKeySecret = ""
    SignName = ""
    TemplateCode = ""


class AliPayKey:
    APP_ID = ""
    GATEWAY_DEV = "https://openapi.alipaydev.com/gateway.do"
    GATEWAY = "https://openapi.alipay.com/gateway.do"

    @staticmethod
    def app_private_key():
        return open("Utils/keys/app_private_key.pem").read()

    @staticmethod
    def alipay_public_key():
        return open("Utils/keys/alipay_public_key.pem").read()
