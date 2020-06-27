from admin_setup import views
from django.conf.urls import url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
app_name='admin_setup'
urlpatterns = [
	path('admin_signin', views.admin_signin,name='admin_signin'),
	path('admin_index', views.admin_index,name='admin_index'),
	path('admin_logout', views.admin_logout,name='admin_logout'),

	path('admin_viewcourse', views.admin_viewcourse,name='admin_viewcourse'),
	url(r'^admin_courses_details/(?P<id>\d+)$', views.admin_courses_details,name='admin_courses_details'),
	path('admin_createcourse', views.admin_createcourse,name='admin_createcourse'),
	url(r'^admin_create_newcourse_ajax/$', views.admin_create_newcourse_ajax,name='admin_create_newcourse_ajax'),
	url(r'^admin_delete_course/(?P<id>\d+)$', views.admin_delete_course,name='admin_delete_course'),
	url(r'^admin_edit_course_deatails/(?P<id>\d+)$', views.admin_edit_course_deatails,name='admin_edit_course_deatails'),
	url(r'^admin_edit_course_content/(?P<id>\d+)$', views.admin_edit_course_content,name='admin_edit_course_content'),
	url(r'^admin_edit_add_topic/(?P<id>\d+)$', views.admin_edit_add_topic,name='admin_edit_add_topic'),
	
	path('admin_viewstudent', views.admin_viewstudent,name='admin_viewstudent'),
	url(r'^admin_view_student_details/(?P<id>\d+)$', views.admin_view_student_details,name='admin_view_student_details'),
	url(r'^admin_delete_student/(?P<id>\d+)$', views.admin_delete_student,name='admin_delete_student'),
	
	path('admin_payments', views.admin_payments,name='admin_payments'),
	path('admin_reports', views.admin_reports,name='admin_reports'),
	path('admin_tests', views.admin_tests,name='admin_tests'),

	path('admin_message', views.admin_message,name='admin_message'),	
	url(r'^admin_doubt_reply/(?P<id>\d+)$', views.admin_doubt_reply,name='admin_doubt_reply'),
	url(r'^admin_chat/(?P<id>\d+)$', views.admin_chat,name='admin_chat'),
	
	path('admin_certificates', views.admin_certificates,name='admin_certificates'),
	url(r'^admin_add_certificates/(?P<id>\d+)$', views.admin_add_certificates,name='admin_add_certificates'),
	url(r'^issue_certificate/(?P<id>\d+)$', views.issue_certificate,name='issue_certificate'),

	path('admin_reviews', views.admin_reviews,name='admin_reviews'),
	path('admin_earnings', views.admin_earnings,name='admin_earnings'),
	path('admin_settings', views.admin_settings,name='admin_settings'),
	url(r'^table_ajax/$', views.table_ajax,name='table_ajax'),


]+ static(settings.MEDIA_URL, 
                              document_root=settings.MEDIA_ROOT) 