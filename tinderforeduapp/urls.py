from . import views
from django.urls import path
from django.conf.urls import url
from django.conf.urls import include
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, \
                                      PasswordResetDoneView, PasswordResetConfirmView, \
                                      PasswordResetCompleteView

app_name = 'tinder'
urlpatterns = [
    path('chat/', include('chat.urls')),
    path('', views.homepage, name='home'),
    path('login/', LoginView.as_view(), name="login"),
    path('add_image/', views.add_image, name="add_image"),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('delete_subject/', views.delete_subject, name='delete_subject'),
    path('match_request/', views.match_request, name="match_request"),
    path('students_list/', views.students_list, name="students_list"),
    path("logout/", LogoutView.as_view(next_page='/login'), name="logout"),
    path('fb_data/', views.facebook_additional_data_request, name='fb_data'),
    path('faq/', TemplateView.as_view(template_name="tinder/faq.html"), name='faq'),
    path('aboutus/', TemplateView.as_view(template_name="tinder/aboutus.html"), name='aboutus'),
    path('privacypolicy/', TemplateView.as_view(template_name="tinder/privacy.html"), name='privacy'),
    path('<int:user_id>/match/', views.match, name="match"),
    path('<int:user_id>/unmatch/', views.unmatch, name="unmatched"),
    path('<int:user_id>/profile/', views.searched_profile, name='profile'),
    path('<int:user_id>/accept_request/', views.accept_request, name="accept_request"),
    path('<int:user_id>/create_comment/', views.create_comment, name='create_comment'),
    path('<int:user_id>/delete_comment/', views.delete_comment, name='delete_comment'),
    path('<int:user_id>/matched_profile/', views.matched_profile, name="matched_profile"),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^password_reset/$', PasswordResetView.as_view(), name='password_reset'),
    url(r'^reset/done/$', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    url(r'^password_reset/done/$', PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.confirmation_email_income, name='confirmation_email_income'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
