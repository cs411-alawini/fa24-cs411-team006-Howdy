# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Healthdata(models.Model):
    userid = models.OneToOneField('User', models.CASCADE, db_column='UserID', primary_key=True)  # Field name made lowercase.
    bmi = models.FloatField(db_column='BMI', blank=True, null=True)  # Field name made lowercase.
    bloodpressure = models.FloatField(db_column='BloodPressure', blank=True, null=True)  # Field name made lowercase.
    heartrate = models.FloatField(db_column='HeartRate', blank=True, null=True)  # Field name made lowercase.
    bodytemperature = models.FloatField(db_column='BodyTemperature', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HealthData'


class Recommendation(models.Model):
    userid = models.OneToOneField('User', models.CASCADE, db_column='UserID', primary_key=True)  # Field name made lowercase.
    recommendstr = models.CharField(db_column='RecommendStr', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sleepdisorder = models.CharField(db_column='SleepDisorder', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Recommendation'


class Sleepdata(models.Model):
    userid = models.OneToOneField('User', models.CASCADE, db_column='UserID', primary_key=True)  # Field name made lowercase.
    sleepduration = models.FloatField(db_column='SleepDuration', blank=True, null=True)  # Field name made lowercase.
    bedtimeconsistency = models.FloatField(db_column='BedtimeConsistency', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SleepData'


class Sleepqualitydata(models.Model):
    userid = models.OneToOneField('User', models.CASCADE, db_column='UserID', primary_key=True)  # Field name made lowercase.
    sleepqualityscore = models.FloatField(db_column='SleepQualityScore', blank=True, null=True)  # Field name made lowercase.
    lightexposurehours = models.FloatField(db_column='LightExposureHours', blank=True, null=True)  # Field name made lowercase.
    movementduringsleep = models.FloatField(db_column='MovementDuringSleep', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SleepQualityData'


class User(models.Model):
    userid = models.IntegerField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=255)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=50, blank=True, null=True)  # Field name made lowercase.
    age = models.IntegerField(db_column='Age', blank=True, null=True)  # Field name made lowercase.
    contactinfo = models.CharField(db_column='ContactInfo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    occupation = models.CharField(db_column='Occupation', max_length=255, blank=True, null=True)  # Field name made lowercase.
    consent = models.IntegerField(db_column='Consent', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'User'


class Userbehavior(models.Model):
    userid = models.OneToOneField(User, models.CASCADE, db_column='UserID', primary_key=True)  # Field name made lowercase.
    physicalactivitylevel = models.IntegerField(db_column='PhysicalActivityLevel', blank=True, null=True)  # Field name made lowercase.
    dailysteps = models.IntegerField(db_column='DailySteps', blank=True, null=True)  # Field name made lowercase.
    caffeineintakemg = models.FloatField(db_column='CaffeineIntakeMg', blank=True, null=True)  # Field name made lowercase.
    stresslevel = models.FloatField(db_column='StressLevel', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserBehavior'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
