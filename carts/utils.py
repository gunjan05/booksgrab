from django.conf import settings
from instamojo_wrapper import Instamojo
from django.urls import reverse


API_KEY= getattr(settings, 'INSTAMOJO_API_KEY', None)
AUTH_TOKEN= getattr(settings, 'INSTAMOJO_AUTH_TOKEN', None)
api = Instamojo(api_key=API_KEY, auth_token=AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/')

class InstamojoPayment(object):
    def make_payment_request(self, request, amount, order_id, email, buyer_name, phone):
        response = api.payment_request_create(
                amount=amount,
                purpose='For Order ID: {}'.format(order_id),
                email=email,
                buyer_name=buyer_name,
                phone=phone,
                allow_repeated_payments=False,
                redirect_url=request.build_absolute_uri(reverse("cart:success")),
                # webhook='http://requestbin.fullcontact.com/w6nv7mw6',
                )
        return response

    def get_payment_details(self, request):
        response = api.payment_request_payment_status('[PAYMENT REQUEST ID]', '[PAYMENT ID]')
        print(response['payment_request']['purpose'])            # Purpose of Payment Request
        print(response['payment_request']['payment']['status'])  # Payment status
