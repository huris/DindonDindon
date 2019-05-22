from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

from Utils.keys.Key import SMSAPIKey as APIKey


class SMS:

    def __init__(self):
        self.client = AcsClient(APIKey.AccessKey_ID, APIKey.AccessKeySecret, 'default')
        self.request = CommonRequest()
        self.request.set_accept_format('json')
        self.request.set_domain('dysmsapi.aliyuncs.com')
        self.request.set_method('POST')
        self.request.set_protocol_type('https')  # https | http
        self.request.set_version('2017-05-25')
        self.request.set_action_name('SendSms')

    def send_sms(self, phone_num, code):
        self.request.add_query_param('PhoneNumbers', phone_num)
        self.request.add_query_param('SignName', APIKey.SignName)
        self.request.add_query_param('TemplateCode', APIKey.TemplateCode)
        code_json = '{"code": "' + code + '"}'
        self.request.add_query_param('TemplateParam', code_json)

        return self.client.do_action_with_exception(self.request)
