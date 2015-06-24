from django.http import HttpResponse
from django.shortcuts import render
from django.utils import simplejson
from payments.models import Charge
import stripe


def donate_index(request):
    """ public key is in payments.js file """
    stripe.api_key = "sk_test_bD1Ol81vyl1cfdKXZxY8jPHf"
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
