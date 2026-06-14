from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views import View

from .forms import RegisterForm, LoginForm


class RegisterView(View):
    template_name = 'users/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('diary:entry_list')

        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                f'Добро пожаловать, {user.username}! Аккаунт создан.'
            )
            return redirect('diary:entry_list')

        return render(request, self.template_name, {'form': form})


class LoginView(View):
    template_name = 'users/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('diary:entry_list')

        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Вы вошли как {user.username}')

                next_url = request.GET.get('next', 'diary:entry_list')
                return redirect(next_url)
            else:
                messages.error(request, 'Неверное имя пользователя или пароль')

        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.info(request, 'Вы вышли из системы')
        return redirect('users:login')
