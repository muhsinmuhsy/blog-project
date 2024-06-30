from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('your-blogs/', views.your_blogs_view, name='your_blogs'),
    path('add-blog/', views.add_blog_view, name='add_blog'),
    path('blog/<int:blog_id>/', views.blog_details_view, name='blog_details'),
    path('edit-blog/<int:blog_id>/', views.edit_blog_view, name='edit_blog'),
    path('delete-blog/<int:blog_id>/', views.delete_blog_view, name='delete_blog'),

    path('api/register/', api.RegisterAPIView.as_view(), name='api_register'),
    path('api/login/', api.LoginAPIView.as_view(), name='api_login'),
    path('api/logout/', api.LogoutAPIView.as_view(), name='api_logout'),
    path('api/blogposts/', api.BlogPostListView.as_view(), name='blogpost-list'),
    path('api/blogposts/create/', api.BlogPostCreateView.as_view(), name='blogpost-create'),
    path('api/blogposts/<int:pk>/', api.BlogPostDetailView.as_view(), name='blogpost-detail'),
    path('api/blogposts/<int:pk>/update/', api.BlogPostUpdateView.as_view(), name='blogpost-update'),
    path('api/blogposts/<int:pk>/delete/', api.BlogPostDeleteView.as_view(), name='blogpost-delete')
]
