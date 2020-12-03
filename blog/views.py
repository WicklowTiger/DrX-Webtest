from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from Users.models import Appointment
from .models import Post, Service


def home(request):
    return render(request, 'blog/home.html')


class PostListView(ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 6


class AppListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Appointment
    template_name = 'blog/appointments.html'
    context_object_name = 'appointments'
    ordering = ['-pk']
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_superuser


class ServiceListView(ListView):
    model = Service
    template_name = 'blog/services.html'
    context_object_name = 'services'
    ordering = ['-pk']
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_superuser


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class ServiceDetailView(DetailView):
    model = Service


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ServiceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Service
    fields = ["title", "price", "content", "image"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser


class ServiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Service
    fields = ["title", "price", "content", "image"]

    def test_func(self):
        return self.request.user.is_superuser


class ServiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Service
    success_url = '/'

    def test_func(self):
        return self.request.user.is_superuser


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


def about(request):
    return render(request, 'blog/about.html', {'title': 'DrX - About'})


def contact(request):
    return render(request, 'blog/contact.html', {'title': 'DrX - Contact'})


def blog(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/blog.html', context, {'title': 'DrX - News'})


def confirm_appointment(request, operation, pk):
    app = Appointment.objects.get(pk=pk)
    if operation == "confirm":
        app.Status = "confirmed"
        send_mail(
            'Appointment confirmed',
            f'Hi {app.user.username}!\n    We have confirmed your appointment!\nKind Regards, \nDrX and Team',
            'drx.webtest@gmail.com',
            [app.user.email],
        )
    elif operation == "cancel":
        app.Status = "cancelled"
        send_mail(
            'Appointment cancelled',
            f'Hi {app.user.username}!\n    We have cancelled your appointment! Please call us if this has caused confusion!\nKind Regards, \nDrX and Team',
            'drx.webtest@gmail.com',
            [app.user.email],
        )
    app.save()
    return redirect("apps")
