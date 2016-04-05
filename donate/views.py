import json
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import simplejson
from django.views.generic import FormView
from payments.models import Charge
import stripe
from .forms import DonateForm
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings

def donate_index(request):
    """ public key is in payments.js file """
    # stripe.api_key = "sk_test_bD1Ol81vyl1cfdKXZxY8jPHf"
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.POST:
        token = request.POST['stripeToken']
        stripe_amount = request.POST['stripe_amount']
        stripe_amount = '%d00' % int(stripe_amount)
        if stripe_amount == 0.00:
            stripe_amount = request.POST['payment']
            stripe_amount = '%d00' % int(stripe_amount)
        try:
            stripe.Charge.create(
                amount=stripe_amount,  # amount in cents
                currency="usd",
                source=token,
                description='Payment from a website'
            )
            data = {
                'success': True,
            }
            return HttpResponse(simplejson.dumps(data), content_type='application/json')
        except stripe.error.CardError, e:
            print 'The card has been declined'
            print e
            pass
    return render(request, 'donate.html', {})


class DonateView(FormView):
    """ Extended page for donations. Using DonateForm """
    template_name = 'donate-extended.html'
    form_class = DonateForm

    def get_context_data(self, **kwargs):
        context = super(DonateView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        data = {
            'success': True
        }
        return HttpResponse(simplejson.dumps(data), content_type='application/json')

    def form_invalid(self, form):
        # html = render_to_string(self.template_name, self.get_context_data(form=form))
        html = json.dumps(form.errors)
        data = {
            'success': False,
            'html': html
        }
        return HttpResponse(simplejson.dumps(data), content_type='application/json')

    def render_to_response(self, context, **response_kwargs):
        return super(DonateView, self).render_to_response(context, **response_kwargs)

def donate_paypal(request):

    # What you want the button to do.
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "10.00",
        "item_name": "Donation to Sikh National Archives",
        "invoice": "unique-invoice-id",
        "notify_url": reverse('paypal-ipn'),
        "return_url": "/donate/",
        "cancel_return": "h/",

    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "paypal.html", context)

