from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('api/v1/users/', views.UserListCreate.as_view()),
    path('api/v1/users/<int:pk>/', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
