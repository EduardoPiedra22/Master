from django.urls import path

from Core.User.views import *

urlpatterns = [
    path('lista/', UserListView.as_view(), name = 'User_lista'),
    path('add/', UserCreateView.as_view(), name = 'User_crear'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name = 'User_editar'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name = 'User_delete'),
    path('change/group/<int:pk>/', UserChangeGropus.as_view(), name='user_change_group'),
    path('profile/', UserProfileView.as_view(), name = 'User_profile'),
    path('change/password/', UserChangePasswordView.as_view(), name='User_change_password'),

]

