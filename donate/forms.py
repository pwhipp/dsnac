import stripe

from django import forms
from .models import Donate, IN_MEMORY_CHOICES


MONTH_CHOICES = (
    (1, 'JAN'),
    (2, 'FEB'),
    (3, 'MAR'),
    (4, 'APR'),
    (5, 'MAY'),
    (6, 'JUN'),
    (7, 'JUL'),
    (8, 'AUG'),
    (9, 'SEP'),
    (10, 'OCT'),
    (11, 'NOV'),
    (12, 'DEC'),

)

YEAR_CHOICES = (
    (16, '2016'),
    (17, '2017'),
    (18, '2018'),
    (19, '2019'),
    (20, '2020'),
    (21, '2021'),
)


class DonateForm(forms.ModelForm):
    memory_of_type = forms.ChoiceField(choices=IN_MEMORY_CHOICES, widget=forms.RadioSelect(), required=False)
    first_name_memory = forms.CharField(required=False)
    first_name_memory.widget.attrs['placeholder'] = 'First Name'
    last_name_memory = forms.CharField(required=False)
    last_name_memory.widget.attrs['placeholder'] = 'Last Name'
    full_name_notification = forms.CharField(required=False)
    full_name_notification.widget.attrs['placeholder'] = 'Full Name'
    recipient_notification = forms.CharField(required=False)
    recipient_notification.widget.attrs['placeholder'] = "Recipient's Email"
    from_notification = forms.CharField(required=False)
    from_notification.widget.attrs['placeholder'] = "From"
    anonymous = forms.BooleanField(required=False)
    message_notification = forms.CharField(widget=forms.Textarea(attrs={'placeholder': '',
                                                                        'rows': 4}), required=False)
    cc_first_name = forms.CharField()
    cc_first_name.widget.attrs['placeholder'] = 'First Name'
    cc_last_name = forms.CharField()
    cc_last_name.widget.attrs['placeholder'] = 'Last Name'
    cc_number = forms.CharField()
    cc_number.widget.attrs['placeholder'] = 'Card Number'
    cc_number.widget.attrs['maxlength'] = 16
    cc_code = forms.CharField()
    cc_code.widget.attrs['placeholder'] = 'Security Code'
    cc_code.widget.attrs['maxlength'] = 3
    exp_date_month = forms.ChoiceField(choices=MONTH_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control'}))

    exp_date_year = forms.ChoiceField(choices=YEAR_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control'}))

    bill_street = forms.CharField()
    bill_street.widget.attrs['placeholder'] = 'Street Address'
    bill_city = forms.CharField()
    bill_city.widget.attrs['placeholder'] = 'City'
    bill_zip = forms.CharField()
    bill_zip.widget.attrs['placeholder'] = 'ZIP / Postal'
    bill_apt = forms.CharField()
    bill_apt.widget.attrs['placeholder'] = 'Apt / Suite #'
    bill_state = forms.CharField()
    bill_state.widget.attrs['placeholder'] = 'Select a State'
    bill_country = forms.CharField()
    bill_country.widget.attrs['placeholder'] = 'Select a Country'

    first_name = forms.CharField()
    first_name.widget.attrs['placeholder'] = 'Your First Name'
    last_name = forms.CharField()
    last_name.widget.attrs['placeholder'] = 'Your Last Name'

    email = forms.CharField(required=False)
    email.widget.attrs['placeholder'] = 'Your Email'
    phone = forms.CharField(required=False)
    phone.widget.attrs['placeholder'] = 'Your Phone Number'

    # widget=forms.PasswordInput()
    password1 = forms.CharField(required=False)
    password1.widget.attrs['placeholder'] = 'Your Password'
    password2 = forms.CharField(required=False)
    password2.widget.attrs['placeholder'] = 'Repeat Password'

    def __init__(self, user, *args, **kwargs):
        kwargs.setdefault('initial', {})
        if user.is_authenticated():
            kwargs['initial']['email'] = user.email
            kwargs['initial']['first_name'] = user.first_name
            kwargs['initial']['last_name'] = user.last_name

            kwargs['initial']['cc_number'] = 'XXXX-XXXX-XXXX-%s' % user.profile.card_last
            kwargs['initial']['cc_first_name'] = user.profile.first_name
            kwargs['initial']['cc_last_name'] = user.profile.last_name
            kwargs['initial']['cc_code'] = 'XXX'
            self.fields['cc_code'].widget.attrs['readonly'] = True

        super(DonateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Donate
        exclude = ('added', 'user')



