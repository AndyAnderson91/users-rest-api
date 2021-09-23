from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import ObtainAuthToken


urlpatterns = [
    path('api/v1/users/', views.UsersList.as_view(), name='users_list'),
    path('api/v1/users/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)



# urlpatterns +=[
#     url(r'^api-token-auth/', ObtainAuthToken.as_view(), name='get_auth_token')
# ]