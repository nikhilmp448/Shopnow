from django.db import models
from shopapp.models import Account
# Create your models here.
class Coupon(models.Model):
    
    coupon_code    = models.CharField(max_length=200, unique=True)
    is_available   = models.BooleanField(default=True)
    quantity       = models.IntegerField()
    amount         = models.IntegerField(default=50)
    created        = models.DateTimeField(auto_now_add=True)

    def _str_(self): 
        return self.coupon_code


class CouponUsers(models.Model):

    coupon       = models.ForeignKey(Coupon, on_delete= models.CASCADE)
    user         = models.ForeignKey(Account, on_delete= models.CASCADE)
    is_used      = models.BooleanField(default=False)
    date_used    = models.DateTimeField(auto_now_add=True)
    amount       = models.IntegerField(null=True)

    def _str_(self): 
        return self.user.email