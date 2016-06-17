import json
import stripe

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.template.loader import render_to_string
from django.utils import simplejson
from django.views.generic import FormView
from django.conf import settings
from django.forms.util import ErrorList
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from paypal.standard.forms import PayPalPaymentsForm

from userprofile.models import Profile
from .forms import DonateForm
from .models import Donate


def donate_index(request):
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
                amount=stripe_amount,
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

        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        fullname = '%s %s' % (first_name, last_name)
        payment = int(form.cleaned_data['amount'])
        print (payment)
        print(type(payment))

        try:
            token = stripe.Token.create(card={
                "number": form.cleaned_data['cc_number'],
                "exp_month": form.cleaned_data["exp_date_month"],
                "exp_year": form.cleaned_data["exp_date_year"],
                "cvc": form.cleaned_data['cc_code'],
                'name': fullname,
            },)
        except Exception as e:
            errors = form._errors.setdefault("cc_number", ErrorList())
            errors.append(e)
            return self.form_invalid(form)

        customer = stripe.Customer.create(source=token.id, description="Donation from  %s" % fullname)

        user = User.objects.create_user(username=form.cleaned_data['email'], email=form.cleaned_data['email'],
                                        password=form.cleaned_data['password1'])

        card = customer['sources']['data'][0]
        subscribe = False
        if form.cleaned_data.get('subscribe'):
            subscribe = True

        profile = Profile.objects.create(user=user, first_name=first_name, last_name=last_name,
                                         stripe_id=customer['id'], default_card=customer['default_source'],
                                         card_last=card['last4'],
                                         card_expiry='%s/%s' % (str(card['exp_month']), str(card['exp_year'])),
                                         subscribe=subscribe, payment_active=True)

        donate = Donate.objects.create(user=profile, amount=payment,
                                       memory_of=form.cleaned_data['memory_of'],
                                       memory_of_type=form.cleaned_data['memory_of_type'],
                                       first_name_memory=form.cleaned_data['first_name_memory'],
                                       last_name_memory=form.cleaned_data['last_name_memory'],
                                       full_name_notification=form.cleaned_data['full_name_notification'],
                                       from_notification=form.cleaned_data['from_notification'],
                                       recipient_notification=form.cleaned_data['recipient_notification'],
                                       anonymous=form.cleaned_data['anonymous'],
                                       message_notification=form.cleaned_data['message_notification'],
                                       cc_first_name=form.cleaned_data['cc_first_name'],
                                       cc_last_name=form.cleaned_data['cc_last_name'],
                                       bill_street=form.cleaned_data['bill_street'],
                                       bill_city=form.cleaned_data['bill_city'],
                                       bill_zip=form.cleaned_data['bill_zip'],
                                       bill_apt=form.cleaned_data['bill_apt'],
                                       bill_state=form.cleaned_data['bill_state'],
                                       bill_country=form.cleaned_data['bill_country'],
                                       monthly_gift=form.cleaned_data['monthly_gift']
                                       )

        try:
            stripe.Charge.create(
                amount=payment * 100,
                currency="usd",
                customer=profile.stripe_id,
                description="Charge for donation #%s" % donate.id,
            )
        except Exception as e:
            errors = form._errors.setdefault("cc_number", ErrorList())
            errors.append(e)
            return self.form_invalid(form)

        return redirect('donation', donation_id=donate.id)


def donation(request, donation_id):
    donation = get_object_or_404(Donate, id=donation_id)
    return render(request, 'thank-donation.html', {'donation': donation})


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

