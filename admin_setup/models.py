from django.db import models

# Create your models here.
class course_details(models.Model):
	course_title=models.CharField(max_length=50)
	course_description=models.TextField()
	course_price=models.CharField(max_length=50)
	course_image=models.ImageField(upload_to = 'course_image')
	
class course_details_dummy(models.Model):
	course_title=models.CharField(max_length=50)
	course_description=models.TextField()
	course_price=models.CharField(max_length=50)
	course_image=models.ImageField(upload_to = 'course_image')

class topic(models.Model):
	course_detail_id=models.IntegerField()
	topic_title=models.CharField(max_length=50)
	topic_part_count=models.CharField(max_length=15)

class chapter(models.Model):
	course_detail_id=models.IntegerField()
	topic_no=models.CharField(max_length=15)
	chapter_title=models.CharField(max_length=50)
	chapter_ulr=models.TextField()
	chapter_file=models.FileField(upload_to = 'course_file')

class certificates(models.Model):
	course_id=models.IntegerField()
	student_id=models.IntegerField()
	certificate=models.FileField(upload_to = 'certificates')

	