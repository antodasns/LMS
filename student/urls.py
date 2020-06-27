from student import views
from django.conf.urls import url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
app_name='student'
urlpatterns = [
	path('stu_register', views.stu_register,name='stu_register'),
	path('', views.stu_signin,name='stu_signin'),
	path('user_logout', views.user_logout,name='user_logout'),
	path('stu_index', views.stu_index,name='stu_index'),

	path('stu_courses', views.stu_courses,name='stu_courses'),
	url(r'^stu_courses_details/(?P<id>\d+)$', views.stu_courses_details,name='stu_courses_details'),
	url(r'^stu_payout/(?P<id>\d+)$', views.stu_payout,name='stu_payout'),
	url(r'^stu_course_buy/(?P<id>\d+)$', views.stu_course_buy,name='stu_course_buy'),
	url(r'^stu_purchase_courses_details/(?P<id>\d+)$', views.stu_purchase_courses_details,name='stu_purchase_courses_details'),
	path('stu_purchased_courses', views.stu_purchased_courses,name='stu_purchased_courses'),

	path('stu_message', views.stu_message,name='stu_message'),	
	url(r'^stu_doubt_message/(?P<id>\d+)$', views.stu_doubt_message,name='stu_doubt_message'),
	url(r'^stu_chat/(?P<id>\d+)$', views.stu_chat,name='stu_chat'),
	url(r'^stu_chat2/(?P<id>\d+)$', views.stu_chat2,name='stu_chat2'),

	path('stu_certificate', views.stu_certificate,name='stu_certificate'),
	path('stu_statement', views.stu_statement,name='stu_statement'),
	url(r'^stu_invoice/(?P<id>\d+)$', views.stu_invoice,name='stu_invoice'),
	path('stu_setting', views.stu_setting,name='stu_setting'),
	path('stu_help', views.stu_help,name='stu_help'),
	path('error_404', views.error_404,name='error_404'),
	# path('videoplayer', views.videoplayer,name='videoplayer'),
	url(r'^videoplayer/(?P<id>\d+)$', views.videoplayer,name='videoplayer'),

]+ static(settings.MEDIA_URL, 
                              document_root=settings.MEDIA_ROOT) 