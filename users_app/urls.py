from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


app_name = 'users_app'
urlpatterns = [
    path('api/users/', views.UserListCreate.as_view(), name='user_list_create'),
    path('api/users/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('', views.IndexRedirectView.as_view(), name='index_redirect'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
