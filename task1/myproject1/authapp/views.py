from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserAccount

def home(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        name = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if UserAccount.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('home')

        UserAccount.objects.create(name=name, email=email, password=password)
        messages.success(request, 'Account created successfully!')
        return redirect('home')

    return redirect('home')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = UserAccount.objects.get(email=email, password=password)
           
            # Save user in session
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            # return render(request,'dashboard.html')
            return redirect('dashboard')
        except UserAccount.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return redirect('home')

    return redirect('home')

def logout_view(request):
    request.session.flush()
    return redirect('home')

def dashboard(request):
    user_name = request.session.get('user_name')
    if not user_name:
        return redirect('home')
    return render(request, 'dashboard.html', {'user_name': user_name})
