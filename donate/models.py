from django.db import models

IN_MEMORY_CHOICES = (
    ('1', 'In Honor Of'),
    ('2', 'In Memory Of'),
)

class Donate(models.Model):
    amount = models.CharField(max_length=255)
    memory_of = models.BooleanField(default=False)
    memory_of_type = models.CharField(max_length=255, choices=IN_MEMORY_CHOICES, blank=True, null=True)
    first_name_memory = models.CharField(max_length=255, blank=True, null=True)
    last_name_memory = models.CharField(max_length=255, blank=True, null=True)
    full_name_notification = models.CharField(max_length=255, blank=True, null=True)
    from_notification = models.CharField(max_length=255, blank=True, null=True)
    recipient_notification = models.CharField(max_length=255, blank=True, null=True)
    anonymous = models.BooleanField(default=True)
    message_notification = models.CharField(max_length=255, blank=True, null=True)
    cc_first_name = models.CharField(max_length=255)
    cc_last_name = models.CharField(max_length=255)
    cc_number = models.PositiveIntegerField(max_length=16)
    cc_code = models.PositiveIntegerField(max_length=3)
    exp_date_month = models.PositiveIntegerField(max_length=2)
    exp_date_year = models.PositiveIntegerField(max_length=2)
    bill_street = models.CharField(max_length=255)
    bill_city = models.CharField(max_length=255)
    bill_zip = models.CharField(max_length=255)
    bill_apt = models.CharField(max_length=255, blank=True, null=True)
    bill_state = models.CharField(max_length=255)
    bill_country = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    monthly_gift = models.BooleanField(default=True)
    subscribe = models.BooleanField(default=True)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Donation'
        verbose_name_plural = 'Donations'

    def __unicode__(self):
        return self.email

