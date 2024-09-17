from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Post,Comment,CustomUser

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content','image']
        widgets = {
            'content': forms.Textarea(attrs={'row':4,'class':'form-control'}), #attrs htmldeki haline özellikler atıyo <textarea name="content" rows="4" class="form-control"></textarea>
            'image': forms.ClearableFileInput(attrs={'class':'form-control-file'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content','parent']
        widgets = {
            'content': forms.Textarea(attrs={'row':3,'placeholder':'yorum yaz..'})
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username','email','password1','password2')

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder':'Username'})
        self.fields['email'].widget.attrs.update({'placeholder':'Email'})
        self.fields['password1'].widget.attrs.update({'placeholder':'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder':'Confirm Password'})
        self.fields['username'].help_text=None
        self.fields['email'].help_text=None
        self.fields['password1'].help_text=None
        self.fields['password2'].help_text=None

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu email zaten kullanılıyor')
        return email


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields= ('username','email','bio','location','profile_picture')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Bu email zaten kullanılıyor')
        return email


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username',widget=forms.TextInput(attrs={'autofocus':True}))
    password = forms.CharField(label='Password',widget=forms.PasswordInput)

    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].widget.attrs.update({'placeholder':'username'})
        self.fields['password'].widget.attrs.update({'placeholder':'password'})