from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django_recaptcha.fields import ReCaptchaField

from .utils import get_institution_choices

SECTOR_CHOICES = [
    ('', '— Select Sector —'),
    ('Technology', 'Technology'),
    ('Finance', 'Finance'),
    ('Healthcare', 'Healthcare'),
    ('Education', 'Education'),
    ('Manufacturing', 'Manufacturing'),
    ('Agriculture', 'Agriculture'),
    ('Media', 'Media & Creative'),
    ('Consulting', 'Consulting'),
    ('NGO', 'NGO / Non-profit'),
    ('Government', 'Government'),
    ('Other', 'Other'),
]

SIZE_CHOICES = [
    ('', '— Select Size —'),
    ('1-10', '1–10 employees'),
    ('11-50', '11–50 employees'),
    ('51-200', '51–200 employees'),
    ('201-500', '201–500 employees'),
    ('500+', '500+ employees'),
]


class StudentRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))
    institution = forms.ChoiceField(choices=[])
    admission_number = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Admission Number'}))
    course = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'e.g. BSc Computer Science'}))
    year_of_study = forms.IntegerField(min_value=1, max_value=8, widget=forms.NumberInput(attrs={'placeholder': 'Year (1-8)'}))
    profile_photo = forms.ImageField(required=False)
    captcha = ReCaptchaField()

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username', 'institution', 'admission_number',
                  'course', 'year_of_study', 'profile_photo', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['institution'].choices = get_institution_choices()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.portal_type = CustomUser.PORTAL_STUDENT
        if commit:
            user.save()
        return user


class EmployerRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Contact Person Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Business Email'}))
    company_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Company Name'}))
    sector = forms.ChoiceField(choices=SECTOR_CHOICES)
    company_size = forms.ChoiceField(choices=SIZE_CHOICES)
    kra_pin = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'KRA PIN (optional)'}))
    website = forms.URLField(required=False, widget=forms.URLInput(attrs={'placeholder': 'https://yourcompany.com'}))
    company_logo = forms.ImageField(required=False)
    captcha = ReCaptchaField()

    class Meta:
        model = CustomUser
        fields = ['first_name', 'email', 'username', 'company_name', 'sector',
                  'company_size', 'kra_pin', 'website', 'company_logo', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.portal_type = CustomUser.PORTAL_EMPLOYER
        if commit:
            user.save()
        return user


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'bio', 'phone', 'location', 'institution', 'admission_number',
                  'course', 'year_of_study', 'graduation_year', 'skills',
                  'linkedin_url', 'github_url', 'portfolio_url', 'profile_photo', 'open_to_work']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'skills': forms.TextInput(attrs={'placeholder': 'Python, Django, React, ...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['institution'].widget = forms.Select(choices=get_institution_choices())


class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone', 'company_name', 'company_about',
                  'sector', 'company_size', 'kra_pin', 'website', 'location',
                  'company_logo', 'actively_hiring']
        widgets = {
            'company_about': forms.Textarea(attrs={'rows': 4}),
        }


class LoginForm(AuthenticationForm):
    captcha = ReCaptchaField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username or Email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})
