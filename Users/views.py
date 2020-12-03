from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from .forms import BookingCreateForm
from .models import Appointment
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'successfully created an account for user: {username}!')
            return redirect('blog-home')
    else:
        form = UserRegistrationForm()
    return render(request, 'Users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'Users/profile.html', context)


@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = BookingCreateForm(request.POST)
        if form.is_valid():
            for app in Appointment.objects.all():
                if app.user == request.user and app.Status == "pending":
                    messages.error(request, f'You already have a pending appointment!', extra_tags="danger")
                    return redirect('book')
            form.instance.user = request.user
            form.save()
            send_mail(
                'Appointment received',
                f'Hi {request.user.username}!\n    We have received your appointment and will be back to you shortly!\nKind Regards, \nDrX and Team',
                'drx.webtest@gmail.com',
                [request.user.email],
            )
            messages.success(request, f'Successfully created an appointment!')
            return redirect('blog-home')
    else:
        form = BookingCreateForm()
    return render(request, 'Users/bookingform.html', {'form': form})