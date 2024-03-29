from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('profile_list/', views.profile_list, name="profile_list"),
    path('profile/<int:pk>/', views.profile, name="profile"),
    path('login/', views.login_user, name="login"), 
    path('logout/', views.logout_user, name="logout"), 
    path('register/', views.register_user, name="register"), 
    path('update_user/', views.update_user, name="update_user"), 
    path('tea_like/<int:pk>', views.tea_like, name="tea_like"),
    path('tea_show/<int:pk>', views.tea_show, name="tea_show"),
    path('unfollow/<int:pk>', views.unfollow, name="unfollow"),
    path('follow/<int:pk>', views.follow, name="follow"),
    path('profile/followers/<int:pk>/', views.followers, name="followers"),
    path('profile/follows/<int:pk>/', views.follows, name="follows"),
    path('delete_tea/<int:pk>', views.delete_tea, name="delete_tea"),
    path('edit_tea/<int:pk>', views.edit_tea, name="edit_tea"),
    path('search/', views.search, name="search"), 
    path('search_user/', views.search_user, name="search_user"), 
]
