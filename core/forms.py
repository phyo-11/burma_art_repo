from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from . models import Profile


class UserInfoForm(forms.ModelForm):
	phone = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Phone'}), required=False)
	address1 = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Address 1'}), required=False)
	address2 = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Address 2'}), required=False)
	zipcode = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Zipcode'}), required=False)
	city = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'City'}), required=False)
	state = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'State'}), required=False)	
	country = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Country'}), required=False)

	class Meta:
		model = Profile
		fields = ('phone','address1','address2','zipcode','city','state','country',)


class ChangePasswordForm(SetPasswordForm):
	class Meta:
		model = User
		fields = ['new_password1', 'new_password2']

	def __init__(self, *args, **kwargs):
		super(ChangePasswordForm, self).__init__(*args, **kwargs)

		
		self.fields['new_password1'].widget.attrs['class'] = 'form-control'
		self.fields['new_password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['new_password1'].label = ''
		self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li>Required: This field is mandatory, so make sure to fill it in!.</li><li>Minimum length: It should be at least 8 characters long.</li><li>No numbers only: Your password can’t be entirely made up of numbers, like 12345678.</li><li>No similarity with username: your password cannot be too similar to your username.</li></ul>'

		self.fields['new_password2'].widget.attrs['class'] = 'form-control'
		self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['new_password2'].label = ''
		self.fields['new_password2'].help_text = '<ul class="form-text text-muted small"><li>Password confirmation: You’ll need to type your password twice, and both entries must match exactly.</li></ul>'




class UpdateUserForm(UserChangeForm):
	#Hide password stuff
	password = None
	#Get other fields
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), required=False)
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}), required=False)
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), required=False)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email',)

	def __init__(self, *args, **kwargs):
		super(UpdateUserForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<ul class="form-text text-muted small"><li>Required: This field is mandatory, so make sure to fill it in!.</li><li>Must be unique: Choose a username that hasn’t already been taken.</li><li>Length: Your username can be up to 150 characters long.</li><li>Allowed characters: You can use letters, numbers, underscores (_), and hyphens (-).</li></ul>'

	


class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), required=False)
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}), required=False)
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), required=False)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<ul class="form-text text-muted small"><li>Required: This field is mandatory, so make sure to fill it in!.</li><li>Must be unique: Choose a username that hasn’t already been taken.</li><li>Length: Your username can be up to 150 characters long.</li><li>Allowed characters: You can use letters, numbers, underscores (_), and hyphens (-).</li></ul>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Required: This field is mandatory, so make sure to fill it in!.</li><li>Minimum length: It should be at least 8 characters long.</li><li>No numbers only: Your password can’t be entirely made up of numbers, like 12345678.</li><li>No similarity with username: your password cannot be too similar to your username.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<ul class="form-text text-muted small"><li>Password confirmation: You’ll need to type your password twice, and both entries must match exactly.</li></ul>'






# class SignUpForm(UserCreationForm):
# 	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
# 	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
# 	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

# 	class Meta:
# 		model = User
# 		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

# 	def __init__(self, *args, **kwargs):
# 		super(SignUpForm, self).__init__(*args, **kwargs)

# 		self.fields['username'].widget.attrs['class'] = 'form-control'
# 		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
# 		self.fields['username'].label = ''
# 		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

# 		self.fields['password1'].widget.attrs['class'] = 'form-control'
# 		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
# 		self.fields['password1'].label = ''
# 		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

# 		self.fields['password2'].widget.attrs['class'] = 'form-control'
# 		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
# 		self.fields['password2'].label = ''




