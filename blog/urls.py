from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, AppListView, ServiceCreateView, ServiceListView, ServiceDeleteView, ServiceUpdateView, ServiceDetailView
from . import views


urlpatterns = [
    path('', views.home, name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('services/new/', ServiceCreateView.as_view(), name='service-create'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
    path('services/<int:pk>/update', ServiceUpdateView.as_view(), name='service-update'),
    path('services/<int:pk>/delete', ServiceDeleteView.as_view(), name='service-delete'),
    path('about/', views.about, name='blog-about'),
    path('contact/', views.contact, name='contact'),
    path('blog/', PostListView.as_view(), name='blog-blog'),
    path('apps/', AppListView.as_view(), name='apps'),
    path('services/', ServiceListView.as_view(), name='services'),
    path('confirm_app/<str:operation>/<int:pk>', views.confirm_appointment, name="cfm_app")
]
