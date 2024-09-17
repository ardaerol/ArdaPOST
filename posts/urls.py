from django.urls import path
from . import views 
app_name='posts'

urlpatterns = [
    path('',views.post_list,name='post_list'),
    path('register/',views.register,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('post/create/',views.create_post,name='create_post'),
    path('post/edit/<int:post_id>',views.edit_post,name='edit_post'),
    path('post/delete/<int:post_id>',views.delete_post,name='delete_post'),
    path('post/like/<int:post_id>',views.like_post,name='like_post'),
    path('post/share/<int:post_id>',views.share_post,name='share_post'),
    path('post/<int:post_id>/comment/add/',views.add_comment,name='add_comment'),
    path('comment/<int:comment_id>/edit',views.edit_comment,name='edit_comment'),
    path('comment/<int:comment_id>/delete',views.delete_comment,name='delete_comment'),
]