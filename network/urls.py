
from django.urls import path, re_path

from . import views

urlpatterns = [
    # Views`
    path('', views.index, name='index'),
    path('profile/<int:author_id>/', views.profile, name='profile'),
    path('following/<str:username>/', views.following, name='following'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),

    # API's
    path('posts', views.submit_post, name='submit_post'),
    path('posts/<int:post_id>', views.get_post, name='get_post'),
    path('posts/<int:postid>/<int:addlike>', views.add_like, name='add_like'),
    path('posts/likes', views.get_likes, name='get_likes'),
    re_path(r'^follow/(?P<authorid>[1-9][0-9]*)/(?P<isfollow>true|false)/$',
        views.follow, name='follow')

]
