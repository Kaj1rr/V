from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, ApplicationForm, ReviewForm
from .models import Application, TransportType

def register(request):
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.email = form.cleaned_data['email']
            user.save()
            
            request.session['phone'] = form.cleaned_data['phone']
            request.session['birth_date'] = str(form.cleaned_data['birth_date'])
            
            messages.success(request, 'Регистрация успешно завершена!')
            return redirect('login')
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})

def user_login(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Пожалуйста, заполните все поля')
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Неверный логин или пароль')
    
    return render(request, 'login.html')

@login_required
def dashboard(request):
    
    applications = request.user.applications.all()
    
    for app in applications:
        app.can_review = (app.status == 'completed' and not app.review)
    
    if request.method == 'POST':
        app_id = request.POST.get('application_id')
        review_text = request.POST.get('review')
        
        if app_id and review_text:
            application = get_object_or_404(Application, id=app_id, user=request.user)
            if application.status == 'completed' and not application.review:
                application.review = review_text
                application.save()
                messages.success(request, 'Спасибо за ваш отзыв!')
                return redirect('dashboard')
    
    return render(request, 'dashboard.html', {'applications': applications})

@login_required
def create_application(request):
  
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, 'Заявка успешно создана! Ожидайте подтверждения администратора.')
            return redirect('dashboard')
    else:
        form = ApplicationForm()
    
    return render(request, 'create_application.html', {'form': form})

def admin_panel(request):
    if request.user.is_authenticated:
        if request.user.username != 'Admin26':
            messages.error(request, 'У вас нет доступа к панели администратора')
            return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            if username == 'Admin26' and password == 'Demo20':
                from django.contrib.auth.models import User
                admin_user, created = User.objects.get_or_create(
                    username='Admin26',
                    defaults={
                        'is_staff': True,
                        'is_superuser': True
                    }
                )
                if created:
                    admin_user.set_password('Demo20')
                    admin_user.save()
                
                login(request, admin_user)
                return redirect('admin_panel')
            else:
                messages.error(request, 'Неверный логин или пароль администратора')
    
    applications = Application.objects.all().select_related('user', 'transport_type')
    
    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    # Сортировка
    sort_by = request.GET.get('sort')
    if sort_by == 'date_asc':
        applications = applications.order_by('created_at')
    elif sort_by == 'date_desc':
        applications = applications.order_by('-created_at')
    elif sort_by == 'user':
        applications = applications.order_by('user__username')
    
    if request.method == 'POST':
        app_id = request.POST.get('application_id')
        new_status = request.POST.get('status')
        
        if app_id and new_status:
            application = get_object_or_404(Application, id=app_id)
            application.status = new_status
            application.save()
            messages.success(request, f'Статус заявки #{app_id} обновлён на "{application.get_status_display()}"')
            return redirect('admin_panel')
    
    return render(request, 'admin_panel.html', {
        'applications': applications,
        'status_filter': status_filter,
        'sort_by': sort_by,
        'status_choices': Application.STATUS_CHOICES
    })

def logout_view(request):
    logout(request)
    return redirect('login')

# Create your views here.
