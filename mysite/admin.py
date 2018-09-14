from django.contrib import admin

from mysite import models

# Register your models here.
class RoomUseConditionAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'room_start_use_date', 'room_end_use_date','booker_name',
    'booking_time', 'booker_phone', 'booker_email', 'confirmed')
    ordering = ('-room_start_use_date',)

class HolidayAdmin(admin.ModelAdmin):
    list_display = ('holiday_name', 'holiday_date')
    ordering = ('-holiday_date',)

class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('file',)

admin.site.register(models.price_multifier)
admin.site.register(models.room_use_condition, RoomUseConditionAdmin)
admin.site.register(models.room_types)
admin.site.register(models.holidays, HolidayAdmin)
admin.site.register(models.FileUpload, FileUploadAdmin)