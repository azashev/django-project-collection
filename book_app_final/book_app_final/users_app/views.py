from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView
from django.contrib.auth import views as auth_views, mixins as auth_mixins, login

from book_app_final.users_app.forms import SignUpForm
from book_app_final.users_app.models import Profile, CustomUser


class UserRegisterView(FormView):
    form_class = SignUpForm
    template_name = 'user_templates/register_user.html'
    success_url = reverse_lazy('homepage')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('homepage')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()

        Profile.objects.create(user=user)

        login(self.request, user)
        next_url = self.request.GET.get('next', '')

        if next_url:
            return redirect(next_url)
        return super().form_valid(form)


class UserLoginView(auth_views.LoginView):
    template_name = 'user_templates/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('homepage')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')
        return context


class ProfileView(auth_mixins.LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'user_templates/profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, username=self.request.user.username)


class ProfileUpdateView(auth_mixins.LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['bio', 'location', 'birth_date']
    template_name = 'user_templates/profile_update.html'
    success_url = reverse_lazy('profile')

    def get_object(self, *args, **kwargs):
        return self.request.user.profile

