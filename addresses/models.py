from django.db import models
from billing.models import BillingProfile


ADDRESS_TYPES=(
('shipping','Shipping address'),
)

STATES_CHOICES=(
('Karnataka', 'Karnataka'), ('Andhra Pradesh', 'Andhra Pradesh'), ('Kerala', 'Kerala'), ('Tamil Nadu', 'Tamil Nadu'), ('Maharashtra', 'Maharashtra'), ('Uttar Pradesh', 'Uttar Pradesh'), ('Goa', 'Goa'), ('Gujarat', 'Gujarat'), ('Rajasthan', 'Rajasthan'), ('Himachal Pradesh', 'Himachal Pradesh'),
('Jammu and Kashmir', 'Jammu and Kashmir'), ('Telangana', 'Telangana'), ('Arunachal Pradesh', 'Arunachal Pradesh'), ('Assam', 'Assam'), ('Bihar', 'Bihar'), ('Chattisgarh', 'Chattisgarh'), ('Haryana', 'Haryana'), ('Madhya Pradesh', 'Madhya Pradesh'), ('Manipur', 'Manipur'),
('Meghalaya', 'Meghalaya'), ('Mizoram', 'Mizoram'), ('Nagaland', 'Nagaland'), ('Orissa', 'Orissa'), ('Punjab', 'Punjab'), ('Sikkim', 'Sikkim'), ('Tripura', 'Tripura'), ('Uttarakhand', 'Uttarakhand'), ('West Bengal', 'West Bengal'), ('Andaman and Nicobar', 'Andaman and Nicobar'),
('Chandigarh', 'Chandigarh'), ('Dadra and Nagar Haveli', 'Dadra and Nagar Haveli'), ('Daman and Diu', 'Daman and Diu'), ('Delhi', 'Delhi'), ('Lakshadweep', 'Lakshadweep'), ('Pondicherry', 'Pondicherry')
)

class Address(models.Model):
    billing_profile   = models.ForeignKey(BillingProfile)
    address_type      = models.CharField(max_length=50, choices=ADDRESS_TYPES, default='shipping')
    fullname          = models.CharField(max_length=255, default='John Miller')
    address_line_1    = models.CharField(max_length=50)
    address_line_2    = models.CharField(max_length=50, null=True, blank=True)
    state             = models.CharField(max_length=50, choices=STATES_CHOICES)
    country           = models.CharField(max_length=50, default='India')
    city              = models.CharField(max_length=50)
    postal_code       = models.CharField(max_length=6, default='400003')

    def __str__(self):
        return str(self.billing_profile)

    def get_address(self):
        return '{line1}\n{line2},\n{city}.\n{state}, {postal},\n{country}'.format(
        line1 = self.address_line_1,
        line2 = self.address_line_2 or '',
        city = self.city,
        state = self.state,
        postal = str(self.postal_code),
        country = self.country
        )
