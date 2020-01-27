from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, include
from django.conf import settings
from . import views

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
    path('reset-password', PasswordResetView.as_view(), name='password_reset_done'),
    path('reset-password/done', PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset-password/confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password/complete', PasswordResetCompleteView.as_view(), name="password_reset_complete")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)