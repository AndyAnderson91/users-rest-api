from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns



urlpatterns = [
    path('api/v1/users/', views.ListCreateUserView.as_view(), name='users_list'),
    path('api/v1/users/<int:pk>/', views.RetrieveUpdateDestroyUserView.as_view(), name='user_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
