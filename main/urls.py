from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, include
from django.conf import settings
from . import views
from .views import CaptchaPasswordResetView as PasswordResetView

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path("profile", views.profile, name='profile'),
    path("contact", views.contact, name='contact'),
    path("category", views.category, name='category'),
    path("post", views.post, name='post'),
    path("event", views.event, name='event'),
    path("bloglist/", views.index),
    path("submit_comment", views.add_comment),
    path("saveEmail/", views.newsletter),
    path('update-profile', views.update_profile),
    path("gallery/", views.gallery),
    path('about-us/', views.about_us),
    path('logout', views.user_logout),
    path('login', views.login_user),
    path('register', views.register),
    path('reset-password', PasswordResetView.as_view(), name='password_reset'),
    path('reset-password/done', PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset-password/confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(template_name='password-reset.htm', success_url='/?password-reset=true'), name='password_reset_confirm'),
    path('reset-password/complete', PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('new-post', views.new_post, name='new_post'),
    path('edit-post/<int:id>', views.edit_post, name='edit_post'),
    path('delete-post/<int:id>', views.delelte_post, name='delete_post'),
    path('my-posts', views.my_posts, name='mypost'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
