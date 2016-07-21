import stripe
import paypalrestsdk

from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.conf import settings
from django.forms.utils import ErrorList
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login

from paypal.standard.forms import PayPalPaymentsForm

from apps.userprofile.models import Profile
from .forms import DonateForm, CustomerDonateForm
from .models import Donate


# todo: celery charge
# todo: email sending


class DonateView(FormView):
    """ Extended page for donations. Using DonateForm """
    template_name = 'donate-extended.html'
    form_class = DonateForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('donate_customer')
        return super(DonateView, self).get(request, *args, **kwargs)

    def form_valid(self, form):

        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        fullname = '%s %s' % (first_name, last_name)
        payment = int(form.cleaned_data['amount'])

        notify_from = form.cleaned_data.get('from_notification')
        notify_to = list(form.cleaned_data.get('recipient_notification'))
        notify_is_anonymous = form.cleaned_data.get('anonymous')
        notify_from_name = form.cleaned_data.get('full_name_notification')
        notify_message = form.cleaned_data.get('message_notification')

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

        try:
            user = User.objects.create_user(username=form.cleaned_data['email'], email=form.cleaned_data['email'],
                                            password=form.cleaned_data['password1'])
        except IntegrityError:
            errors = form._errors.setdefault("email", ErrorList())
            errors.append('User with this email is already exists. Please log in or recover password if needed.')
            return self.form_invalid(form)

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
                                       full_name_notification=notify_from_name,
                                       from_notification=notify_from,
                                       recipient_notification=notify_to,
                                       anonymous=notify_is_anonymous,
                                       message_notification=notify_message,
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
            donate.delete()
            return self.form_invalid(form)

        if all([notify_from, notify_to]):
            if notify_is_anonymous:
                notify_from = 'donations@sikhnationalarchives.org'
                try:
                    send_mail(
                        'Donation alert from Sikh National Archives',
                        notify_message,
                        notify_from,
                        notify_to,
                        fail_silently=True,
                    )
                except Exception as e:
                    print e

        new_user = authenticate(username=user.username,
                                password=form.cleaned_data['password1'])

        login(self.request, new_user)

        return redirect('donation', donation_id=donate.id)


class CustomerDonateView(FormView):
    template_name = 'donate-customer.html'
    form_class = CustomerDonateForm

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        if not profile.payment_active:
            return redirect('add_card')
        return super(CustomerDonateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        payment = int(form.cleaned_data['amount'])
        notify_from = form.cleaned_data.get('from_notification')
        notify_to = list(form.cleaned_data.get('recipient_notification'))
        notify_is_anonymous = form.cleaned_data.get('anonymous')
        notify_from_name = form.cleaned_data.get('full_name_notification')
        notify_message = form.cleaned_data.get('message_notification')
        profile = Profile.objects.get(user=self.request.user)

        donate = Donate.objects.create(user=profile, amount=payment,
                                       memory_of=form.cleaned_data['memory_of'],
                                       memory_of_type=form.cleaned_data['memory_of_type'],
                                       first_name_memory=form.cleaned_data['first_name_memory'],
                                       last_name_memory=form.cleaned_data['last_name_memory'],
                                       full_name_notification=notify_from_name,
                                       from_notification=notify_from,
                                       recipient_notification=notify_to,
                                       anonymous=notify_is_anonymous,
                                       message_notification=notify_message,
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
            errors = form._errors.setdefault("amount", ErrorList())
            errors.append(e)
            donate.delete()
            return self.form_invalid(form)

        if all([notify_from, notify_to]):
            if notify_is_anonymous:
                notify_from = 'donations@sikhnationalarchives.org'
            try:
                send_mail(
                    'Donation alert from Sikh National Archives',
                    notify_message,
                    notify_from,
                    notify_to,
                    fail_silently=True,
                )
            except Exception as e:
                print e
        return redirect('donation', donation_id=donate.id)


def donation(request, donation_id):
    donation = get_object_or_404(Donate, id=donation_id)
    return render(request, 'thank-donation.html', {'donation': donation})


class PayPalDonateView(FormView):
    """ Extended page for donations. Using DonateForm """
    template_name = 'paypal.html'
    form_class = DonateForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('donate_customer')

        # https://github.com/paypal/PayPal-Python-SDK
        # https://developer.paypal.com/developer/dashboard/sandbox/
        return super(PayPalDonateView, self).get(request, *args, **kwargs)

    def form_valid(self, form):

        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        fullname = '%s %s' % (first_name, last_name)
        payment = int(form.cleaned_data['amount'])

        notify_from = form.cleaned_data.get('from_notification')
        notify_to = list(form.cleaned_data.get('recipient_notification'))
        notify_is_anonymous = form.cleaned_data.get('anonymous')
        notify_from_name = form.cleaned_data.get('full_name_notification')
        notify_message = form.cleaned_data.get('message_notification')

        try:
            user = User.objects.create_user(username=form.cleaned_data['email'], email=form.cleaned_data['email'],
                                            password=form.cleaned_data['password1'])
        except (User.MultipleObjectsReturned, IntegrityError):
            errors = form._errors.setdefault("email", ErrorList())
            errors.append('User with this email is already exists. Please log in or recover password if needed.')
            return self.form_invalid(form)

        subscribe = False
        if form.cleaned_data.get('subscribe'):
            subscribe = True

        profile = Profile.objects.create(user=user, first_name=first_name, last_name=last_name,
                                         subscribe=subscribe, payment_active=False)

        donate = Donate.objects.create(user=profile, amount=payment,
                                       memory_of=form.cleaned_data['memory_of'],
                                       memory_of_type=form.cleaned_data['memory_of_type'],
                                       first_name_memory=form.cleaned_data['first_name_memory'],
                                       last_name_memory=form.cleaned_data['last_name_memory'],
                                       full_name_notification=notify_from_name,
                                       from_notification=notify_from,
                                       recipient_notification=notify_to,
                                       anonymous=notify_is_anonymous,
                                       message_notification=notify_message,
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
        paypalrestsdk.configure({
            "mode": "sandbox",  # sandbox or live
            "client_id": settings.PAYPAL_IDENTITY_TOKEN,
            "client_secret": settings.PAYPAL_CLIENT_SECRET})

        payment_dict = {
            "intent": "sale",
            "payer": {
                "payment_method": "credit_card",
                "funding_instruments": [{
                    "credit_card": {
                        "type": "visa",
                        "number": "{}".format(form.cleaned_data['cc_number']),
                        "expire_month": "{}".format(form.cleaned_data["exp_date_month"]),
                        "expire_year": "{}".format(form.cleaned_data["exp_date_year"]),
                        "cvv2": "{}".format(form.cleaned_data['cc_code']),
                        "first_name": "{}".format(first_name),
                        "last_name": "{}".format(last_name)}}]},
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "item",
                        "sku": "item",
                        "price": "{}.00".format(payment),
                        "currency": "USD",
                        "quantity": 1}]},
                "amount": {
                    "total": "{}.00".format(payment),
                    "currency": "USD"},
                "description": "Donation from {} via PayPal".format(fullname)}]
        }

        paypal_payment = paypalrestsdk.Payment(payment_dict)

        if paypal_payment.create():
            print("Payment created successfully")
        else:
            print(paypal_payment.error)

        if all([notify_from, notify_to]):
            if notify_is_anonymous:
                notify_from = 'donations@sikhnationalarchives.org'
                try:
                    send_mail(
                        'Donation alert from Sikh National Archives',
                        notify_message,
                        notify_from,
                        notify_to,
                        fail_silently=True,
                    )
                except Exception as e:
                    print e

        new_user = authenticate(username=user.username,
                                password=form.cleaned_data['password1'])

        login(self.request, new_user)

        return redirect('donation', donation_id=donate.id)


def donate_paypal(request):

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

