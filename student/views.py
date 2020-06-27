from django.shortcuts import render,HttpResponse
from django.http import HttpResponse,HttpResponseRedirect 
from student.models import user_details,course_buy,messages,chat_tocken,user_details_dummy
from admin_setup.models import course_details,course_details_dummy,chapter,topic,certificates
from student.forms import UserForm
from django.contrib.auth import authenticate,login,logout
# from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.
def stu_register(request):
	
	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
			form.save()

			stu_reg=user_details(
				first_name=request.POST['fullname'],
				user_name=request.POST['username'],
				phone=request.POST['phone'],
				email=request.POST['email'],
				password=request.POST['password'],
				login_id=(User.objects.values_list('pk', flat=True).latest('id'))
				)
			stu_reg.save()
			stu_reg_dum=user_details_dummy(
				first_name=request.POST['fullname'],
				user_name=request.POST['username'],
				phone=request.POST['phone'],
				email=request.POST['email'],
				password=request.POST['password'],
				login_id=(User.objects.values_list('pk', flat=True).latest('id'))
				)
			stu_reg_dum.save()
			return HttpResponseRedirect('/')
		
	else:

		form=UserForm()
		
	return render(request,'student/student_register.html',{'form':form})


def user_logout(request):
	
	logout(request)
	return HttpResponseRedirect('/')

def stu_signin(request):
	if request.method == 'POST':
		user_name=request.POST.get('username')
		pass_word=request.POST.get('password')
		current_user=0
		user = authenticate(username=user_name, password=pass_word)
		if user:
			login(request,user)
			current_user=request.user.id
		
			if User.objects.values_list('is_superuser', flat=True).get(pk=current_user)==0 and User.objects.values_list('is_active', flat=True).get(pk=current_user)==1:
				if user:
					login(request,user)
					return HttpResponseRedirect('/stu_index')
				else:
					return render(request,'student/student_signin.html')

	
	return render(request,'student/student_signin.html')

@login_required(login_url='/')
def stu_index(request):
	count=0
	count1=0
	certificate_count=certificates.objects.filter(student_id=request.user.id)
	buy_cou_count=course_buy.objects.filter(student_id=request.user.id)
	for y in certificate_count:
		count1=count1+1
	for x in buy_cou_count:
		count=count+1
	buyed_course=course_buy.objects.filter(student_id=request.user.id).order_by('buy_date')[:2]
	course_title=[]
	course_img=[]
	course_id=[]
	for x in buyed_course:
		course_title.append(course_details.objects.values_list('course_title', flat=True).get(id=x.course_id))
		course_img.append(course_details.objects.values_list('course_image', flat=True).get(id=x.course_id))
		course_id.append(course_details.objects.values_list('id', flat=True).get(id=x.course_id))
	zippy=zip(course_title,course_img,course_id)
	return render(request,'student/student_index.html',{'zippy':zippy,'count':count,'count1':count1})
@login_required(login_url='/')
def stu_courses(request):
	details=course_details_dummy.objects.all()
	return render(request,'student/student_courses.html',{'details':details})


@login_required(login_url='/')
def stu_courses_details(request,id):
	details=course_details.objects.filter(pk=id)
	topic_details=topic.objects.filter(course_detail_id=id)
	chapter_details=chapter.objects.filter(course_detail_id=id)
	return render(request,'student/student_course_detail_view.html',{'details':details,'chapter_details':chapter_details,'topic_details':topic_details})
@login_required(login_url='/')
def stu_payout(request,id):
	buyed_cou=[]
	buyed_course=course_buy.objects.filter(student_id=request.user.id)
	for x in buyed_course:
		buyed_cou.append(x.course_id)
	if id in buyed_cou:
		return HttpResponse("This course already purchased")
	details=course_details.objects.filter(pk=id)
	return render(request,'student/student_payout.html',{'details':details})
@login_required(login_url='/')
def stu_course_buy(request,id):
	stu_buy=course_buy(
		course_id=id,
		student_id=request.user.id
		)
	stu_buy.save()
	return HttpResponseRedirect('/stu_courses')
@login_required(login_url='/')
def stu_purchased_courses(request):
	course_title=[]
	course_img=[]
	course_id=[]
	buyed_course=course_buy.objects.filter(student_id=request.user.id)
	for x in buyed_course:
		course_title.append(course_details.objects.values_list('course_title', flat=True).get(id=x.course_id))
		course_img.append(course_details.objects.values_list('course_image', flat=True).get(id=x.course_id))
		course_id.append(course_details.objects.values_list('id', flat=True).get(id=x.course_id))
	zippy=zip(course_title,course_img,course_id)
	
	return render(request,'student/student_purchase.html',{'zippy':zippy})
@login_required(login_url='/')
def stu_purchase_courses_details(request,id):
	buy_cou=[]
	buyed_course=course_buy.objects.filter(student_id=request.user.id)
	for x in buyed_course:
		buy_cou.append(x.course_id)
	
	if int(id) in buy_cou:
		c_id=id
		c_title=course_details.objects.values_list('course_title', flat=True).get(pk=id)
		c_price=course_details.objects.values_list('course_price', flat=True).get(pk=id)
		c_desc=course_details.objects.values_list('course_description', flat=True).get(pk=id)
		c_img=course_details.objects.values_list('course_image', flat=True).get(pk=id)
		details=course_details.objects.filter(pk=id)
		topic_details=topic.objects.filter(course_detail_id=id)
		chapter_details=chapter.objects.filter(course_detail_id=id)
	else:
		return HttpResponseRedirect('/error_404')
	return render(request,'student/student_purchase_course_detail_view.html',{'details':details,'chapter_details':chapter_details,'topic_details':topic_details,'c_id':c_id,'c_img':c_img,'c_title':c_title,'c_price':c_price,'c_desc':c_desc})
@login_required(login_url='/')
def stu_message(request):
	stu_ids=[]
	for x in chat_tocken.objects.all():
		stu_ids.append(x.student_id)
	if request.user.id in stu_ids:
		c_id=chat_tocken.objects.values_list('course_id', flat=True).filter(student_id=request.user.id).latest('id')
		msg=messages.objects.filter(tocken_id=chat_tocken.objects.values_list('id', flat=True).filter(student_id=request.user.id).latest('id'))
	else:
		c_buy=course_buy.objects.filter(student_id=request.user.id)
		c_detai=course_details.objects.all()
		return render(request,'student/student_messages3.html',{'c_buy':c_buy,'c_detai':c_detai})
	c_buy=course_buy.objects.filter(student_id=request.user.id)
	c_detai=course_details.objects.all()
	return render(request,'student/student_messages.html',{'c_id':c_id,'msg':msg,'c_buy':c_buy,'c_detai':c_detai})
@login_required(login_url='/')
def stu_doubt_message(request,id):
	c_id=id
	c_title=course_details.objects.values_list('course_title', flat=True).get(pk=id)
	tockens=chat_tocken.objects.all()
	for x in tockens:
		if x.course_id==int(id) and x.student_id==request.user.id:
			return HttpResponseRedirect('/stu_chat2/%d'%int(x.id))
	stu_tocken=chat_tocken(
	tocken=1,
	course_id=c_id,
	student_id=request.user.id
	)
	stu_tocken.save()
	c_buy=course_buy.objects.filter(student_id=request.user.id)
	c_detai=course_details.objects.all()
	return render(request,'student/student_messages.html',{'c_title':c_title,'c_id':c_id,'c_buy':c_buy,'c_detai':c_detai})
@login_required(login_url='/')
def stu_chat(request,id):
	c_id=id
	c_title=course_details.objects.values_list('course_title', flat=True).get(pk=id)
	if request.method == 'POST':
		stu_msgs=messages(
		course_id=id,
		stu_admin_ids=request.user.id,
		msg=request.POST['chat_widget_message_text_2'],
		designation='student',
		tocken_id=chat_tocken.objects.values_list('id', flat=True).filter(student_id=request.user.id).latest('id'),
		)
		stu_msgs.save()
		return HttpResponseRedirect('/stu_chat/%d'%int(id))
	c_buy=course_buy.objects.filter(student_id=request.user.id)
	c_detai=course_details.objects.all()
	msg=messages.objects.filter(tocken_id=chat_tocken.objects.values_list('id', flat=True).latest('id'))

	return render(request,'student/student_messages.html',{'c_title':c_title,'c_id':c_id,'msg':msg,'c_buy':c_buy,'c_detai':c_detai})
@login_required(login_url='/')
def stu_chat2(request,id):
	c_id=chat_tocken.objects.values_list('course_id', flat=True).get(pk=id)
	c_title=course_details.objects.values_list('course_title', flat=True).get(pk=chat_tocken.objects.values_list('course_id', flat=True).get(pk=id))
	if request.method == 'POST':
		stu_msgs=messages(
		course_id=chat_tocken.objects.values_list('course_id', flat=True).get(pk=id),
		stu_admin_ids=request.user.id,
		msg=request.POST['chat_widget_message_text_2'],
		designation='student',
		tocken_id=id,
		)
		stu_msgs.save()
		return HttpResponseRedirect('/stu_chat2/%d'%int(id))
	msg=messages.objects.filter(tocken_id=id)
	c_buy=course_buy.objects.filter(student_id=request.user.id)
	c_detai=course_details.objects.all()
	return render(request,'student/student_messages2.html',{'c_title':c_title,'c_id':c_id,'msg':msg,'t_id':int(id),'c_buy':c_buy,'c_detai':c_detai})
@login_required(login_url='/')
def stu_certificate(request):
	course=course_details.objects.all()
	issued_certificates=certificates.objects.filter(student_id=request.user.id)
	
	# for x in issued_certificates:
	# 	course_title.append(course_details.objects.values_list('course_title', flat=True).get(id=x.course_id))
	# zippy=zip(course_title,issued_certificates)
	return render(request,'student/student_my_certificates.html',{'course':course,'issued_certificates':issued_certificates})



@login_required(login_url='/')
def stu_statement(request):
	buyed_course=course_buy.objects.filter(student_id=request.user.id)
	details=course_details.objects.all()
	return render(request,'student/student_statements.html',{'buyed_course':buyed_course,'details':details})
@login_required(login_url='/')
def stu_invoice(request,id):
	buyed_course=course_buy.objects.get(pk=id)
	course_deta=course_details.objects.get(id=buyed_course.course_id)
	student_deta=user_details.objects.get(login_id=buyed_course.student_id)
	# print(student_deta.user_name)
	return render(request,'student/stu_invoice.html',{'course_deta':course_deta,'student_deta':student_deta})
@login_required(login_url='/')
def stu_setting(request):
	# return HttpResponse(request.user.id)
	student_deta=user_details.objects.get(login_id=request.user.id)
	form=UserForm(instance=request.user)
	if request.method == 'POST':
		form = UserForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
		student=user_details.objects.get(login_id=request.user.id)
		student.first_name=request.POST['fullname']
		student.user_name=request.POST['username']
		student.phone=request.POST['phone']
		student.email=request.POST['email']
		student.password=request.POST['password']
		student.save()
		return HttpResponseRedirect('/')
	else:

		form=UserForm(instance=request.user)
	
	return render(request,'student/student_settings.html',{'form':form,'student_deta':student_deta})
@login_required(login_url='/')
def stu_help(request):
	return render(request,'student/student_help.html')
@login_required(login_url='/')
def error_404(request):
	return render(request,'student/error_404.html')

@login_required(login_url='/')
def videoplayer(request,id):
	vdo_url=chapter.objects.values_list('chapter_ulr', flat=True).get(pk=id)
	course_t=course_details.objects.values_list('course_title', flat=True).get(pk=chapter.objects.values_list('course_detail_id', flat=True).get(pk=id))
	topic_t=topic.objects.filter(course_detail_id=chapter.objects.values_list('course_detail_id', flat=True).get(pk=id),topic_part_count=chapter.objects.values_list('topic_no', flat=True).get(pk=id))
	chap_t=chapter.objects.values_list('chapter_title', flat=True).get(pk=id)

	return render(request,'student/videoplayer.html',{'vdo_url':vdo_url,'course_t':course_t,'topic_t':topic_t,'chap_t':chap_t})