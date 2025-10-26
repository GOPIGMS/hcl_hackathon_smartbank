from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Customer, Admin, Auditor, CustomerVerification

admin.site.register(User, UserAdmin)
admin.site.register(Customer)
admin.site.register(Admin)
admin.site.register(Auditor)
admin.site.register(CustomerVerification)
