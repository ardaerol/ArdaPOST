from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Post,Like,Share,CustomUser
from .forms import CustomUserCreationForm,CustomUserChangeForm
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('author','content','created_at','total_likes','total_shares')
    search_fields = ('content',)
    readonly_fields = ('created_at','updated_ad')

class LikeAdmin(admin.ModelAdmin):
    list_display = ('post','user','created_at')


class ShareAdmin(admin.ModelAdmin):
    list_display = ('user','post','created_at')

class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    fieldsets =(
        (None,{'fields':('username','password')}),
        ('Personal info',{'fields':('first_name','last_name','email','bio','location')}),
        ('Permissions',{'fields':('is_active','is_staff','is_superuser')}),
        ('Important dates',{'fields':('last_login','date_joined')}),
    )

    add_fieldsets= (
        (None,{
            'classes':('wide',),
            'fields':('username','email','password1','password2','bio','location')
        })
    )

    list_display = ('username','email','bio','location','is_staff')
    search_fields = ('username','email','bio','location')
    ordering=('username',)

admin.site.register(Post,PostAdmin)
admin.site.register(Like,LikeAdmin)
admin.site.register(Share,ShareAdmin)
admin.site.register(CustomUser,CustomUserAdmin)