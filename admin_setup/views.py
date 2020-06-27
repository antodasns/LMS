from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect 
from django.utils.datastructures import MultiValueDictKeyError
from admin_setup.models import course_details,course_details_dummy,chapter,topic,certificates
from student.models import user_details,user_details_dummy,course_buy,messages,chat_tocken
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json  
from admin_setup.forms import UserForm
# Create your views here.
def admin_signin(request):
	if request.method == 'POST':
		user_name=request.POST.get('username')
		pass_word=request.POST.get('password')
		current_user=0
		user = authenticate(username=user_name, password=pass_word)
		if user:
			login(request,user)
			current_user=request.user.id
		
			if User.objects.values_list('is_superuser', flat=True).get(pk=current_user)==1:
				if user:
					login(request,user)
					return HttpResponseRedirect('/admin_index')
				else:
					return render(request,'admin_setup/admin_signin.html')

	
	return render(request,'admin_setup/admin_signin.html')


def admin_logout(request):
	
	logout(request)
	return HttpResponseRedirect('/admin_signin')

@login_required(login_url='/admin_signin')
def admin_index(request):
	if User.objects.values_list('is_superuser', flat=True).get(pk=request.user.id)==1:
		course_pri=[]
		total_course=course_details.objects.all().count()
		total_student=user_details.objects.all().count()
		total_enroll=course_buy.objects.all().count()
		course_bu=course_buy.objects.all()
		for x in course_bu:
			course_pri.append(int(course_details.objects.values_list('course_price', flat=True).get(pk=x.course_id)))
		total_sales=sum(course_pri)
		new_students=user_details.objects.all().order_by('created_date')[:3]
		return render(request,'admin_setup/admin_index.html',{'total_sales':total_sales,'total_enroll':total_enroll,'total_course':total_course,'total_student':total_student,'new_students':new_students})
	else:
		return HttpResponseRedirect('/error_404')
@login_required(login_url='/admin_signin')
def admin_viewcourse(request):
	if User.objects.values_list('is_superuser', flat=True).get(pk=request.user.id)==1:
		details=course_details_dummy.objects.all()
		return render(request,'admin_setup/admin_view_courses.html',{'details':details})
	else:
		return HttpResponseRedirect('/error_404')
@login_required(login_url='/admin_signin')
def admin_courses_details(request,id):
	if User.objects.values_list('is_superuser', flat=True).get(pk=request.user.id)==1:
		buy_cou=[]
		buyed_course=course_buy.objects.filter(student_id=request.user.id)
		for x in buyed_course:
			buy_cou.append(x.course_id)
		c_id=id
		c_title=course_details.objects.values_list('course_title', flat=True).get(pk=id)
		c_price=course_details.objects.values_list('course_price', flat=True).get(pk=id)
		c_desc=course_details.objects.values_list('course_description', flat=True).get(pk=id)
		c_img=course_details.objects.values_list('course_image', flat=True).get(pk=id)
		details=course_details.objects.filter(pk=id)
		topic_details=topic.objects.filter(course_detail_id=id)
		chapter_details=chapter.objects.filter(course_detail_id=id)
		
		return render(request,'admin_setup/admin_course_detail_view.html',{'details':details,'chapter_details':chapter_details,'topic_details':topic_details,'c_id':c_id,'c_img':c_img,'c_title':c_title,'c_price':c_price,'c_desc':c_desc})
	else:
		return HttpResponseRedirect('/error_404')


@login_required(login_url='/admin_signin')
def admin_createcourse(request):
	if User.objects.values_list('is_superuser', flat=True).get(pk=request.user.id)==1:

		file=[]
		count=0
		if request.method == 'POST':
			cre_course=course_details(
			course_title=request.POST['course_title'],
			course_description=request.POST['course_description'],
			course_price=request.POST['course_price'],
			course_image=request.FILES['course_image']
			)
			cre_course.save()
			cre_course_dum=course_details_dummy(
			course_title=request.POST['course_title'],
			course_description=request.POST['course_description'],
			course_price=request.POST['course_price'],
			course_image=request.FILES['course_image']
			)
			cre_course_dum.save()
			cou=course_details.objects.latest('id')

			file_list=request.FILES.getlist('files')
			for x in request.POST.getlist('files'):
				if x=='yes':
					for y in file_list[:1]:
						print(y)
						file.append(y)
						file_list.pop(0)
				else:
					file.append(x)
			file = list(filter(None, file))

			for a,b,c,d in zip(request.POST.getlist('topic_no'),request.POST.getlist('chapter_title'),request.POST.getlist('video_url'),file):
				
				if d=='no':
					cre_che=chapter(
					course_detail_id=cou.id,
					topic_no=a,
					chapter_title=b,
					chapter_ulr=c,
					)
					cre_che.save()
				else:
					cre_che=chapter(
					course_detail_id=cou.id,
					topic_no=a,
					chapter_title=b,
					chapter_ulr=c,
					chapter_file=d,
					)
					cre_che.save()


			for e,f in zip(request.POST.getlist('topic_title'),request.POST.getlist('topicco_no')):
				cre_top=topic(
				course_detail_id=cou.id,
				topic_title=e,
				topic_part_count=f,
				)
				cre_top.save()

			return HttpResponseRedirect('/admin_createcourse')

		return render(request,'admin_setup/admin_create_newcourse.html')
	else:
		return HttpResponseRedirect('/error_404')
@login_required(login_url='/admin_signin')
def admin_delete_course(request,id):
	if User.objects.values_list('is_superuser', flat=True).get(pk=request.user.id)==1:
		course_det=course_details_dummy.objects.get(pk=id)
		course_det.delete()
		return HttpResponseRedirect('/admin_viewcourse')
	else:
		return HttpResponseRedirect('/error_404')
@login_required(login_url='/admin_signin')
def admin_viewstudent(request):
	if User.objects.values_list('is_superuser', flat=True).get(pk=request.user.id)==1:
		details=user_details_dummy.objects.all()
		return render(request,'admin_setup/admin_view_student.html',{'details':details})
	else:
		return HttpResponseRedirect('/error_404')
@login_required(login_url='/admin_signin')
def admin_view_student_details(request,id):
	if User.objects.values_list('is_superuser', flat=True).get(pk=request.user.id)==1:
		details=user_details.objects.get(login_id=id)
		count=0
		buy_cou_count=course_buy.objects.filter(student_id=id)
		for x in buy_cou_count:
			count=count+1
		buyed_course=course_buy.objects.filter(student_id=id).order_by('buy_date')[:2]
		course_title=[]
		course_img=[]
		course_id=[]
		course_desc=[]
		for x in buyed_course:
			course_title.append(course_details.objects.values_list('course_title', flat=True).get(id=x.course_id))
			course_img.append(course_details.objects.values_list('course_image', flat=True).get(id=x.course_id))
			course_id.append(course_details.objects.values_list('id', flat=True).get(id=x.course_id))
			course_desc.append(course_details.objects.values_list('course_description', flat=True).get(id=x.course_id))
		zippy=zip(course_title,course_img,course_id,course_desc)
		
		return render(request,'admin_setup/admin_view_student_details.html',{'zippy':zippy,'count':count,'details':details})
	else:
		return HttpResponseRedirect('/error_404')
@login_required(login_url='/admin_signin')
def admin_delete_student(request,id):
	if User.objects.values_list('is_superuser', flat=True).get(pk=request.user.id)==1:
		stud_reg = User.objects.filter(pk=int(id)).update(is_active=0)
		stud_det=user_details_dummy.objects.filter(login_id=id)
		stud_det.delete()

		return HttpResponseRedirect('/admin_viewstudent')
	else:
		return HttpResponseRedirect('/error_404')

@login_required(login_url='/admin_signin')
def admin_payments(request):
	if User.objects.values_list('is_superuser', flat=True).get(pk=request.user.id)==1:
		return render(request,'admin_setup/admin_view_payments.html')
	else:
		return HttpResponseRedirect('/error_404')
@login_required(login_url='/admin_signin')
def admin_reports(request):
	if User.objects.values_list('is_superuser', flat=True).get(pk=request.user.id)==1:
		import datetime
		total_sal=[]
		total_enroll=0
		buyed_course=course_buy.objects.filter(buy_date__year=datetime.datetime.now().year,buy_date__month=datetime.datetime.now().month)
		details=user_details.objects.all()
		couse_det=course_details.objects.all()

		for x in buyed_course:
			total_sal.append(int(course_details.objects.values_list('course_price', flat=True).get(id=x.course_id)))
			total_enroll=total_enroll+1
		total_course=course_details.objects.all().count()
		total_student=user_details.objects.all().count()
		if request.method == 'POST':

			import datetime
			total_sal=[]
			total_enroll=0
			buyed_course=course_buy.objects.filter(buy_date__year=request.POST['year'],buy_date__month=request.POST['month'])
			details=user_details.objects.all()
			couse_det=course_details.objects.all()
			
			for x in buyed_course:
				total_sal.append(int(course_details.objects.values_list('course_price', flat=True).get(id=x.course_id)))
				total_enroll=total_enroll+1
			total_course=course_details.objects.all().count()
			total_student=user_details.objects.all().count()
			return render(request,'admin_setup/admin_view_report.html',{'buyed_course':buyed_course,'details':details,'couse_det':couse_det,'total_salery':sum(total_sal),'total_enroll':total_enroll,'total_course':total_course,'total_student':total_student})
		return render(request,'admin_setup/admin_view_report.html',{'buyed_course':buyed_course,'details':details,'couse_det':couse_det,'total_salery':sum(total_sal),'total_enroll':total_enroll,'total_course':total_course,'total_student':total_student})
	else:
		return HttpResponseRedirect('/error_404')
@login_required(login_url='/admin_signin')
def admin_tests(request):
	if User.objects.values_list('is_superuser', flat=True).get(pk=request.user.id)==1:
		return render(request,'admin_setup/admin_tests.html')
	else:
		return HttpResponseRedirect('/error_404')
@login_required(login_url='/admin_signin')
def admin_message(request):
	if User.objects.values_list('is_superuser', flat=True).get(pk=request.user.id)==1:
		msg=messages.objects.all()
		if not msg:
			c_id=1
		else:
			c_id=messages.objects.values_list('course_id', flat=True).latest('id')
		tocken_id=chat_tocken.objects.all().order_by('-id')
		msgs=messages.objects.all()
		stu=user_details.objects.all()
		crs=course_details.objects.all()
		return render(request,'admin_setup/admin_chat.html',{'c_id':c_id,'tocken_id':tocken_id,'msgs':msgs,'crs':crs,'stu':stu})
	else:
		return HttpResponseRedirect('/error_404')
@login_required(login_url='/admin_signin')
def admin_doubt_reply(request,id):
	if User.objects.values_list('is_superuser', flat=True).get(pk=request.user.id)==1:
		c_id=id
		tocken_id=chat_tocken.objects.all().order_by('-id')
		msgs=messages.objects.filter(tocken_id=id)
		c_title=course_details.objects.values_list('course_title', flat=True).get(pk=chat_tocken.objects.values_list('course_id', flat=True).get(pk=id))
		stu_name=user_details.objects.values_list('user_name', flat=True).get(login_id=chat_tocken.objects.values_list('student_id', flat=True).get(pk=id))
		stu=user_details.objects.all()
		crs=course_details.objects.all()
		# return HttpResponse(msgs)
		return render(request,'admin_setup/admin_chat.html',{'c_id':c_id,'tocken_id':tocken_id,'msgs':msgs,'crs':crs,'stu':stu,'c_title':c_title,'stu_name':stu_name})
	else:
		return HttpResponseRedirect('/error_404')
@login_required(login_url='/admin_signin')
def admin_chat(request,id):
	if User.objects.values_list('is_superuser', flat=True).get(pk=request.user.id)==1:
		c_id=id
		tocken_id=chat_tocken.objects.all().order_by('-id')
		msgs=messages.objects.filter(tocken_id=id)
		stu=user_details.objects.all()
		crs=course_details.objects.all()
		c_title=course_details.objects.values_list('course_title', flat=True).get(pk=chat_tocken.objects.values_list('course_id', flat=True).get(pk=id))
		stu_name=user_details.objects.values_list('user_name', flat=True).get(login_id=chat_tocken.objects.values_list('student_id', flat=True).get(pk=id))
		if request.method == 'POST':
			stu_msgs=messages(
			course_id=0,
			stu_admin_ids=request.user.id,
			msg=request.POST['chat_widget_message_text_2'],
			designation='admin',
			tocken_id=id,
			)
			stu_msgs.save()
			return HttpResponseRedirect('/admin_chat/%d'%int(id))
		return render(request,'admin_setup/admin_chat.html',{'c_id':c_id,'tocken_id':tocken_id,'msgs':msgs,'crs':crs,'stu':stu,'c_title':c_title,'stu_name':stu_name})
	else:
		return HttpResponseRedirect('/error_404')


@login_required(login_url='/admin_signin')
def admin_certificates(request):
	if User.objects.values_list('is_superuser', flat=True).get(pk=request.user.id)==1:
		details=user_details.objects.all()
		return render(request,'admin_setup/admin_certificates.html',{'details':details})
	else:
		return HttpResponseRedirect('/error_404')
@login_required(login_url='/admin_signin')
def admin_add_certificates(request,id):
	if User.objects.values_list('is_superuser', flat=True).get(pk=request.user.id)==1:
		details=user_details.objects.get(login_id=id)
		count=0
		buy_cou_count=course_buy.objects.filter(student_id=id)
		isuued=[]
		isuued_final=[]
		for x in buy_cou_count:
			count=count+1
		buyed_course=course_buy.objects.filter(student_id=id).order_by('buy_date')[:2]
		course_title=[]
		course_img=[]
		course_id=[]
		course_desc=[]
		cert=certificates.objects.filter(student_id=id)
		for x in cert:
			isuued.append(x.course_id)
		for x in buyed_course:
			course_title.append(course_details.objects.values_list('course_title', flat=True).get(id=x.course_id))
			course_img.append(course_details.objects.values_list('course_image', flat=True).get(id=x.course_id))
			course_id.append(course_details.objects.values_list('id', flat=True).get(id=x.course_id))
			course_desc.append(course_details.objects.values_list('course_description', flat=True).get(id=x.course_id))
			if x.course_id in isuued:
				isuued_final.append("yes")
			else:
				isuued_final.append("no")
		print(isuued_final)
		zippy=zip(course_title,course_img,course_id,course_desc,isuued_final)
		
		return render(request,'admin_setup/admin_add_certificate.html',{'zippy':zippy,'count':count,'details':details,'cert':cert})
	else:
		return HttpResponseRedirect('/error_404')
@login_required(login_url='/admin_signin')
def issue_certificate(request,id):
	if User.objects.values_list('is_superuser', flat=True).get(pk=request.user.id)==1:
		if request.method == 'POST':
			# return HttpResponse(request.POST['stu_id'])
			stu_cert=certificates(
			course_id=id,
			student_id=request.POST['stu_id'],
			certificate=request.FILES['certi'],
			)
			stu_cert.save()
			return HttpResponseRedirect('/admin_add_certificates/%d'%int(request.POST['stu_id']))
		return render(request,'admin_setup/admin_add_certificate.html')
	else:
		return HttpResponseRedirect('/error_404')
@login_required(login_url='/admin_signin')
def admin_reviews(request):
	if User.objects.values_list('is_superuser', flat=True).get(pk=request.user.id)==1:
		return render(request,'admin_setup/admin_review.html')
	else:
		return HttpResponseRedirect('/error_404')
@login_required(login_url='/admin_signin')
def admin_earnings(request):
	if User.objects.values_list('is_superuser', flat=True).get(pk=request.user.id)==1:
		return render(request,'admin_setup/admin_view_earnings.html')
	else:
		return HttpResponseRedirect('/error_404')
@login_required(login_url='/admin_signin')
def admin_settings(request):
	if User.objects.values_list('is_superuser', flat=True).get(pk=request.user.id)==1:
	# admin_deta=user_details.objects.get(login_id=request.user.id)
		form=UserForm(instance=request.user)
		if request.method == 'POST':
			form = UserForm(request.POST, instance=request.user)
			if form.is_valid():
				form.save()
			return HttpResponseRedirect('/')
		else:

			form=UserForm(instance=request.user)
		
		return render(request,'admin_setup/admin_profile_settings.html',{'form':form})
	else:
		return HttpResponseRedirect('/error_404')
@login_required(login_url='/admin_signin')
def table_ajax(request):
	import datetime
	jan_sal=[0]
	feb_sal=[0]
	mar_sal=[0]
	apr_sal=[0]
	may_sal=[0]
	jun_sal=[0]
	jul_sal=[0]
	aug_sal=[0]
	sep_sal=[0]
	oct_sal=[0]
	nov_sal=[0]
	dec_sal=[0]
	
	jan_course=course_buy.objects.filter(buy_date__year=datetime.datetime.now().year,buy_date__month=1)
	feb_course=course_buy.objects.filter(buy_date__year=datetime.datetime.now().year,buy_date__month=2)
	mar_course=course_buy.objects.filter(buy_date__year=datetime.datetime.now().year,buy_date__month=3)
	apr_course=course_buy.objects.filter(buy_date__year=datetime.datetime.now().year,buy_date__month=4)
	may_course=course_buy.objects.filter(buy_date__year=datetime.datetime.now().year,buy_date__month=5)
	jun_course=course_buy.objects.filter(buy_date__year=datetime.datetime.now().year,buy_date__month=6)
	jul_course=course_buy.objects.filter(buy_date__year=datetime.datetime.now().year,buy_date__month=7)
	aug_course=course_buy.objects.filter(buy_date__year=datetime.datetime.now().year,buy_date__month=8)
	sep_course=course_buy.objects.filter(buy_date__year=datetime.datetime.now().year,buy_date__month=9)
	oct_course=course_buy.objects.filter(buy_date__year=datetime.datetime.now().year,buy_date__month=10)
	nov_course=course_buy.objects.filter(buy_date__year=datetime.datetime.now().year,buy_date__month=11)
	dec_course=course_buy.objects.filter(buy_date__year=datetime.datetime.now().year,buy_date__month=12)

	for x in jan_course:
		jan_sal.append(int(course_details.objects.values_list('course_price', flat=True).get(id=x.course_id)))
	for x in feb_course:
		feb_sal.append(int(course_details.objects.values_list('course_price', flat=True).get(id=x.course_id)))
	for x in mar_course:
		mar_sal.append(int(course_details.objects.values_list('course_price', flat=True).get(id=x.course_id)))
	for x in apr_course:
		apr_sal.append(int(course_details.objects.values_list('course_price', flat=True).get(id=x.course_id)))
	for x in may_course:
		may_sal.append(int(course_details.objects.values_list('course_price', flat=True).get(id=x.course_id)))
	for x in jun_course:
		jun_sal.append(int(course_details.objects.values_list('course_price', flat=True).get(id=x.course_id)))
	for x in jul_course:
		jul_sal.append(int(course_details.objects.values_list('course_price', flat=True).get(id=x.course_id)))
	for x in aug_course:
		aug_sal.append(int(course_details.objects.values_list('course_price', flat=True).get(id=x.course_id)))
	for x in sep_course:
		sep_sal.append(int(course_details.objects.values_list('course_price', flat=True).get(id=x.course_id)))
	for x in oct_course:
		oct_sal.append(int(course_details.objects.values_list('course_price', flat=True).get(id=x.course_id)))
	for x in nov_course:
		nov_sal.append(int(course_details.objects.values_list('course_price', flat=True).get(id=x.course_id)))
	for x in dec_course:
		dec_sal.append(int(course_details.objects.values_list('course_price', flat=True).get(id=x.course_id)))
	



	jsona = json.dumps({'jan':sum(jan_sal),'feb':sum(feb_sal),'mar':sum(mar_sal),'apr':sum(apr_sal),'may':sum(may_sal),'jun':sum(jun_sal),'jul':sum(jul_sal),'aug':sum(aug_sal),'sep':sum(sep_sal),'oct':sum(oct_sal),'nov':sum(nov_sal),'dec':sum(dec_sal)})

	return HttpResponse(jsona, content_type='application/json')



def admin_create_newcourse_ajax(request):
	
	data = json.loads(request.POST.get('data'))
	attr1 = data.get('course_title', None)
	print(attr1)
	jsona = json.dumps({'get_barcode': request.POST.get('data')})
	return HttpResponse(jsona, content_type='application/json')


@login_required(login_url='/admin_signin')
def admin_edit_course_deatails(request,id):
	if User.objects.values_list('is_superuser', flat=True).get(pk=request.user.id)==1:
		details=course_details.objects.get(pk=id)
		if request.method == 'POST':
			if request.FILES.get('course_image')==None:
				
				course_det=course_details.objects.get(pk=id)
				course_det.course_title=request.POST['course_title']
				course_det.course_description=request.POST['course_description']
				course_det.course_price=request.POST['course_price']
				course_det.save()

				course_det=course_details_dummy.objects.get(pk=id)
				course_det.course_title=request.POST['course_title']
				course_det.course_description=request.POST['course_description']
				course_det.course_price=request.POST['course_price']
				course_det.save()
				
				return HttpResponseRedirect('/admin_edit_course_deatails/%d'%int(id))
			
			else:
				
				course_det=course_details.objects.get(pk=id)
				course_det.course_title=request.POST['course_title']
				course_det.course_description=request.POST['course_description']
				course_det.course_price=request.POST['course_price']
				course_det.course_image=request.FILES['course_image']
				course_det.save()

				course_det=course_details_dummy.objects.get(pk=id)
				course_det.course_title=request.POST['course_title']
				course_det.course_description=request.POST['course_description']
				course_det.course_price=request.POST['course_price']
				course_det.course_image=request.FILES['course_image']
				course_det.save()

				return HttpResponseRedirect('/admin_edit_course_deatails/%d'%int(id))

		return render(request,'admin_setup/admin_course_edit_detail.html',{'details':details})
	else:
		return HttpResponseRedirect('/error_404')


@login_required(login_url='/admin_signin')
def admin_edit_course_content(request,id):
	if User.objects.values_list('is_superuser', flat=True).get(pk=request.user.id)==1:
		details=course_details.objects.get(pk=id)
		topic_details=topic.objects.filter(course_detail_id=id)
		chapter_details=chapter.objects.filter(course_detail_id=id)

		file=[]
		count=0
		if request.method == 'POST':
			
			del_chap = list(request.POST.get('del_chapters').split(",")) 
			del_top=list(request.POST.get('del_topics').split(","))

			for x in del_chap[1:]:
				
				chap_det=chapter.objects.filter(pk=int(x))
				chap_det.delete()
			for y in del_top[1:]:
				top_det=topic.objects.filter(pk=int(y))
				top_det.delete()
			
			file_list=request.FILES.getlist('files')
			for x in request.POST.getlist('files'):
				if x=='yes':
					for y in file_list[:1]:
						print(y)
						file.append(y)
						file_list.pop(0)
				else:
					file.append(x)
			file = list(filter(None, file))

			for a,b,c,d,ch_id in zip(request.POST.getlist('topic_no'),request.POST.getlist('chapter_title'),request.POST.getlist('video_url'),file,request.POST.getlist('chapter_id')):

				if d=='no':
					chap_det=chapter.objects.get(pk=int(ch_id))
					chap_det.course_detail_id=id
					chap_det.topic_no=a
					chap_det.chapter_title=b
					chap_det.chapter_ulr=c
					chap_det.save()
				else:
					chap_det=chapter.objects.get(pk=int(ch_id))
					chap_det.course_detail_id=id
					chap_det.topic_no=a
					chap_det.chapter_title=b
					chap_det.chapter_ulr=c
					chap_det.chapter_file=d
					chap_det.save()

			
			for e,f,tp_id in zip(request.POST.getlist('topic_title'),request.POST.getlist('topicco_no'),request.POST.getlist('topic_id')):
				
				top_det=topic.objects.get(pk=int(tp_id))
				top_det.course_detail_id=id
				top_det.topic_title=e
				top_det.topic_part_count=f
				top_det.save()
				

			return HttpResponseRedirect('/admin_edit_course_content/%d'%int(id))
		return render(request,'admin_setup/admin_course_edit_content.html',{'details':details,'topic_details':topic_details,"chapter_details":chapter_details})
	else:
		return HttpResponseRedirect('/error_404')


@login_required(login_url='/admin_signin')
def admin_edit_add_topic(request,id):
	if User.objects.values_list('is_superuser', flat=True).get(pk=request.user.id)==1:
		details=course_details.objects.get(pk=id)
		topic_c=topic.objects.filter(course_detail_id=id).latest('topic_part_count')
		topic_c=int(topic_c.topic_part_count)

		file=[]
		count=0
		if request.method == 'POST':
			# return HttpResponse(request.POST.getlist('topic_no'))
			file_list=request.FILES.getlist('files')
			for x in request.POST.getlist('files'):
				if x=='yes':
					for y in file_list[:1]:
						print(y)
						file.append(y)
						file_list.pop(0)
				else:
					file.append(x)
			file = list(filter(None, file))

			for a,b,c,d in zip(request.POST.getlist('topic_no'),request.POST.getlist('chapter_title'),request.POST.getlist('video_url'),file):
				
				if d=='no':
					cre_che=chapter(
					course_detail_id=id,
					topic_no=a,
					chapter_title=b,
					chapter_ulr=c,
					)
					cre_che.save()
				else:
					cre_che=chapter(
					course_detail_id=id,
					topic_no=a,
					chapter_title=b,
					chapter_ulr=c,
					chapter_file=d,
					)
					cre_che.save()


			for e,f in zip(request.POST.getlist('topic_title'),request.POST.getlist('topicco_no')):
				cre_top=topic(
				course_detail_id=id,
				topic_title=e,
				topic_part_count=f,
				)
				cre_top.save()

			return HttpResponseRedirect('/admin_edit_add_topic/%d'%int(id))
		return render(request,'admin_setup/admin_course_edit_topics_add.html',{'details':details,'topic_c':topic_c})
	else:
		return HttpResponseRedirect('/error_404')