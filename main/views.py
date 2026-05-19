from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Application
from .forms import (
    RegistrationForm, LoginForm, ApplicationForm, ReviewForm
)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        user = User.objects.create_user(
            username=data['login'],
            password=data['password'],
            full_name=data['full_name'],
            phone=data['phone'],
            email=data['email'],
        )
        login(request, user)
        return redirect('profile')
    return render(request, 'main/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    form = LoginForm(request.POST or None)
    error = None
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        user = authenticate(
            request, username=data['login'], password=data['password']
        )
        if user is not None:
            login(request, user)
            return redirect('profile')
        error = 'Неверный логин или пароль'
    return render(request, 'main/login.html', {
        'form': form, 'error': error
    })


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    if request.user.username == 'Admin26':
        return redirect('admin_panel')
    applications = request.user.applications.all()
    review_form = ReviewForm()
    can_review = applications.filter(status='completed').exclude(
        review__isnull=False
    ).exists()

    if request.method == 'POST' and 'review_text' in request.POST:
        app_id = request.POST.get('application_id')
        app = get_object_or_404(
            Application, id=app_id, user=request.user,
            status='completed', review__isnull=True
        )
        form = ReviewForm(request.POST)
        if form.is_valid():
            from .models import Review
            Review.objects.create(
                application=app, text=form.cleaned_data['text']
            )
            messages.success(request, 'Отзыв добавлен')
            return redirect('profile')

    return render(request, 'main/profile.html', {
        'applications': applications,
        'review_form': review_form,
        'can_review': can_review,
    })


@login_required
def apply_view(request):
    if request.user.username == 'Admin26':
        return redirect('admin_panel')
    form = ApplicationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        app = form.save(commit=False)
        app.user = request.user
        app.save()
        messages.success(request, 'Заявка отправлена на согласование')
        return redirect('profile')
    return render(request, 'main/apply.html', {'form': form})


@login_required
def admin_panel_view(request):
    if request.user.username != 'Admin26':
        return redirect('profile')

    status_filter = request.GET.get('status', '')
    sort_by = request.GET.get('sort', '-created_at')
    applications = Application.objects.all()

    if status_filter:
        applications = applications.filter(status=status_filter)

    valid_sorts = {
        'created_at': 'created_at',
        '-created_at': '-created_at',
        'status': 'status',
        '-status': '-status',
        'user': 'user__username',
        '-user': '-user__username',
    }
    sort = valid_sorts.get(sort_by, '-created_at')
    applications = applications.order_by(sort)

    from django.core.paginator import Paginator
    paginator = Paginator(applications, 5)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)

    if request.method == 'POST' and 'change_status' in request.POST:
        app_id = request.POST.get('application_id')
        new_status = request.POST.get('new_status')
        app = get_object_or_404(Application, id=app_id)
        if new_status in dict(Application.STATUS_CHOICES):
            app.status = new_status
            app.save()
            messages.success(request, f'Статус заявки #{app.id} изменен')
        return redirect(request.path)

    return render(request, 'main/admin_panel.html', {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'current_sort': sort_by,
        'status_choices': Application.STATUS_CHOICES,
    })
