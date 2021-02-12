from django.urls import path, re_path
from rest_framework_simplejwt import views as jwt_views
from . import views


urlpatterns = [
    path('',views.home, name="home"),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', views.UserList.as_view(), name="users_list"),
    path('api/users/create/', views.CreateUserView.as_view(), name="create_user"),
    path('api/users/change_password/', views.ChangePasswordView.as_view()),
    path('api/users/update/', views.UpdateProfileView.as_view()),
    re_path(r'^api/users/(?P<id>\d+)$', views.UserDetail.as_view()),
]
