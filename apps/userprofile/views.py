import stripe
from django.forms.utils import ErrorList

from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.db.models import Sum

from apps.donate.models import Donate
from apps.bookreader.models import FavoriteBook, BookReading
from .forms import CreditCardForm
from models import Profile


def dashboard(request):
    if request.user.is_authenticated():
        try:
            Profile.objects.get(user=request.user)
            user = request.user
            transactions = Donate.objects.filter(user=user.profile)
            favorite_books = FavoriteBook.objects.filter(user=user)
            # total = Donate.objects.filter(user=user.profile).aggregate(Sum('amount'))
            # todo: change `amount` field to integer and use Sum
            all_amounts = Donate.objects.filter(user=user.profile).values_list('amount', flat=True)
            total = 0
            for amount in all_amounts:
                try:
                    donation = int(amount)
                    total += donation
                except ValueError:
                    pass
            reading = BookReading.objects.filter(user=user)

            card_is_invalid = False
            if not user.profile.payment_active:
                card_is_invalid = True

            if not user.profile.default_card:
                card_is_invalid = True

            data = {
                'user': user,
                'transactions': transactions,
                'favorite_books': favorite_books,
                'total': total,
                'reading': reading,
                'card_is_invalid': card_is_invalid
            }
            return render(request, 'dashboard.html', data)
        except Profile.DoesNotExist:
            Profile.objects.create(user=request.user, first_name=request.user.first_name,
                                   last_name=request.user.last_name, subscribe=True)
            return redirect('dashboard')
    return render(request, 'dashboard.html', {})


class ChangeCardView(FormView):
    template_name = 'add_card.html'
    success_url = '/profile/dashboard/'
    form_class = CreditCardForm

    def form_valid(self, form):
        try:
            token = stripe.Token.create(card={
                "number": form.cleaned_data['card_number'],
                "exp_month": form.cleaned_data["expiration"].month,
                "exp_year": form.cleaned_data["expiration"].year,
                "cvc": form.cleaned_data['cvc'],
            },)
        except Exception as e:
            errors = form._errors.setdefault("card_number", ErrorList())
            errors.append(e._message)
            return self.form_invalid(form)

        try:
            customer = stripe.Customer.create(source=token.id,
                                              description="Payment for  %s %s" %
                                                          (self.request.user.profile.first_name,
                                                           self.request.user.profile.last_name))
        except Exception as e:
            errors = form._errors.setdefault("card_number", ErrorList())
            errors.append(e._message)
            return self.form_invalid(form)



        user = Profile.objects.get(user=self.request.user)
        user.stripe_id = customer['id']
        user.default_card = customer['default_source']
        card = customer['sources']['data'][0]
        user.card_last = card['last4']
        user.card_expiry = '{}/{}'.format(str(card['exp_month']),
                                          str(card['exp_year']))
        user.payment_active = True
        user.save()

        return super(ChangeCardView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        user = Profile.objects.get(user=self.request.user)
        context = super(ChangeCardView, self).get_context_data(**kwargs)
        context['host'] = user
        return context