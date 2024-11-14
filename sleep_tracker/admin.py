from django.contrib import admin
from .models import User
from .models import Healthdata
from .models import Userbehavior
from .models import Sleepqualitydata
from .models import Sleepdata
from .models import Recommendation
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('userid', 'password', 'gender', 'age', 'contactinfo', 'occupation', 'consent')
    search_fields = list_display
    list_filter = list_display

@admin.register(Healthdata)
class HealthdataAdmin(admin.ModelAdmin):
    list_display = ('userid', 'bmi', 'bloodpressure', 'heartrate', 'bodytemperature')
    search_fields = list_display
    list_filter = list_display


@admin.register(Userbehavior)
class UserbehaviorAdmin(admin.ModelAdmin):
    list_display = ('userid', 'physicalactivitylevel', 'dailysteps', 'caffeineintakemg', 'stresslevel')
    search_fields = list_display
    list_filter = list_display


@admin.register(Sleepqualitydata)
class SleepqualitydataAdmin(admin.ModelAdmin):
    list_display = ('userid', 'sleepqualityscore', 'lightexposurehours', 'movementduringsleep')
    search_fields = list_display
    list_filter = list_display

@admin.register(Sleepdata)
class SleepdataAdmin(admin.ModelAdmin):
    list_display = ('userid', 'sleepduration', 'bedtimeconsistency')
    search_fields = list_display
    list_filter = list_display

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('userid', 'recommendstr', 'sleepdisorder')
    search_fields = list_display
    list_filter = list_display
