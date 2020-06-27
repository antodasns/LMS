from django import forms
# from staff.models import staffs_table
from django.contrib.auth.models import User,Group


class UserForm(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'prompt srch_explore','placeholder':'Password'}))
	# role=forms.ModelChoiceField(queryset=Group.objects.all(),widget=forms.Select(attrs={'class':'form-control',}))
	confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'prompt srch_explore','placeholder':'Confirm Password'}))
	class Meta:
		model=User
		fields=['username','email','password']
		widgets = {
           
           
            'username': forms.TextInput(attrs={'class':'prompt srch_explore','placeholder':'UserName'}),
            'email': forms.TextInput(attrs={'class':'prompt srch_explore','placeholder':'Email'}),
          
        }

		label={'password':'Password'}

	def clean(self):
		cleaned_data = super(UserForm, self).clean()
		password = cleaned_data.get("password")
		confirm_password = cleaned_data.get("confirm_password")


		min_length = 6
		if len(password) < min_length:
			msg = 'Password must be at least %s characters long.' %(str(min_length))
			self.add_error('password', msg)

		
		
		if password != confirm_password:
			raise forms.ValidationError(
				"password and confirm_password does not match"
				)
		return self.cleaned_data
	# def __init__(self,*args,**kwargs):
	# 	if kwargs.get('instance'):
	# 		initial=kwargs.setdefault('initial',{})
	# 		if kwargs['instance'].groups.all():
	# 			initial['role']=kwargs['instance'].groups.all()[0]
	# 		else:
	# 			initial['role']=None 
	# 	forms.ModelForm.__init__(self,*args,**kwargs)

	def save(self):
		password=self.cleaned_data.pop('password')
		# role=self.cleaned_data.pop('role')
		u=super().save()
		# u.groups.set([role])
		u.set_password(password)
		u.save()
		return u

 
