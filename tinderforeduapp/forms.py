from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, UserInfo, ProfilePic


# form for signup page
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    college = forms.CharField(max_length=100)
    gender = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=150)
    age = forms.CharField(max_length=10)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'age',
                  'email', 'college', 'gender',)


# form for comment section
class CommentForm(forms.ModelForm):
    star_score = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ]
    star = forms.CharField(label="Choose your score", widget=forms.Select(choices=star_score))

    class Meta:
        model = Comment
        fields = ('comment', 'star',)


# form for request additional data when user signup with Facebook for the first time
class AdditionalForm(forms.ModelForm):
    school = forms.CharField(max_length=100)

    class Meta:
        model = UserInfo
        fields = ('school',)


# form to edit logged in user profile
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['firstname', 'lastname', 'age', 'school', 'gender', ]


# form to edit logged in user profile picture
class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = ProfilePic
        fields = ['images']


# form to edit logged in user additional picture1
class AddPictureForm(forms.ModelForm):
    class Meta:
        model = ProfilePic
        fields = ['images']
