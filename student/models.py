from django.db import models
from django.utils.timezone import now

# Create your models here.
class user_details(models.Model):
	first_name=models.CharField(max_length=30)
	user_name=models.CharField(max_length=30)
	phone=models.CharField(max_length=30)
	email=models.CharField(max_length=30)
	password=models.CharField(max_length=30)
	created_date = models.DateTimeField(default=now, editable=False)
	login_id=models.IntegerField()

class user_details_dummy(models.Model):
	first_name=models.CharField(max_length=30)
	user_name=models.CharField(max_length=30)
	phone=models.CharField(max_length=30)
	email=models.CharField(max_length=30)
	password=models.CharField(max_length=30)
	created_date = models.DateTimeField(default=now, editable=False)
	login_id=models.IntegerField()

class course_buy(models.Model):
	course_id=models.IntegerField()
	student_id=models.IntegerField()
	buy_date = models.DateTimeField(default=now, editable=False)

class messages(models.Model):
	stu_admin_ids=models.IntegerField()
	course_id=models.IntegerField()
	msg=models.TextField()
	designation=models.CharField(max_length=10)
	tocken_id=models.IntegerField()
	msg_date = models.DateTimeField(default=now, editable=False)


class chat_tocken(models.Model):
	tocken=models.IntegerField()
	course_id=models.IntegerField()
	student_id=models.IntegerField()
	conf_date = models.DateTimeField(default=now, editable=False)