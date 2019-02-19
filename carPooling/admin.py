from django.contrib import admin
from carPooling.models import CarPoolingUserConf,CarPoolingCity,CarPoolingAssDetail
# Register your models here.
@admin.register(CarPoolingCity)
class CarPoolingCityAdmin(admin.ModelAdmin):
    list_display = CarPoolingCity.list_field

@admin.register(CarPoolingUserConf)
class CarPoolingUserConfAdmin(admin.ModelAdmin):
    list_display = CarPoolingUserConf.list_field

@admin.register(CarPoolingAssDetail)
class CarPoolingAssDetailAdmin(admin.ModelAdmin):
    list_display = CarPoolingAssDetail.list_field