from django.contrib import admin
from .models import Manufacturer, Device, DeviceType, DeviceCondition, Firm, Good, Specification, GoodPhoto


admin.site.register(Manufacturer)
admin.site.register(DeviceCondition)
admin.site.register(Firm)
admin.site.register(DeviceType)
admin.site.register(Device)
admin.site.register(Good)
admin.site.register(Specification)
admin.site.register(GoodPhoto)
