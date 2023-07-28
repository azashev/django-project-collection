from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView, DeleteView, TemplateView
from django.contrib.auth import views as auth_views, forms as auth_forms, mixins as auth_mixins, login

from book_app_final.books_app.models import Book
from book_app_final.reviews_app.models import Review
from book_app_final.users_app.forms import SignUpForm, ProfileForm, CustomUserUpdateForm
from book_app_final.users_app.models import Profile, CustomUser, Shelf


class UserRegisterView(FormView):
    template_name = 'user_templates/register_user.html'
    success_url = reverse_lazy('homepage')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('homepage')
        user_form = SignUpForm()
        profile_form = ProfileForm()
        del profile_form.fields['profile_picture']
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)
        del profile_form.fields['profile_picture']

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.is_default_image = True
            profile.save()
            login(request, user)
            return redirect(self.success_url)
        else:
            context = {
                'user_form': user_form,
                'profile_form': profile_form
            }

            return render(request, self.template_name, context)


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

    def form_valid(self, form):
        login(self.request, form.get_user())
        next_url = self.request.GET.get('next', 'homepage')

        return redirect(next_url)


class UserLogoutView(auth_mixins.LoginRequiredMixin, auth_views.LogoutView):
    next_page = 'homepage'


class ProfileView(auth_mixins.LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'user_templates/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user.profile


class ProfileUpdateView(auth_mixins.LoginRequiredMixin, TemplateView):
    template_name = 'user_templates/profile_update.html'
    success_url = reverse_lazy('profile')

    def get_object(self, *args, **kwargs):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        data = super(ProfileUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data["user_form"] = CustomUserUpdateForm(self.request.POST, instance=self.request.user)
            data["form"] = ProfileForm(self.request.POST, self.request.FILES, instance=self.request.user.profile)
        else:
            data["user_form"] = CustomUserUpdateForm(instance=self.request.user)
            data["form"] = ProfileForm(instance=self.request.user.profile)
        data["profile"] = self.request.user.profile

        return data

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        user_form = context['user_form']
        profile_form = context['form']

        if user_form.is_valid() and profile_form.is_valid():
            if 'profile_picture_clear' in request.POST and request.POST['profile_picture_clear'] == 'on':
                profile = request.user.profile
                profile.is_default_image = True
                profile.profile_picture.delete(save=False)
                profile.profile_picture = None
                profile.save()
            else:
                user_form.save()
                profile = profile_form.save(commit=False)
                if 'profile_picture' in request.FILES:
                    profile.is_default_image = False
                profile_form.save()

            return redirect(self.success_url)
        else:
            return self.render_to_response(context)


class ProfileDeleteView(auth_mixins.LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'user_templates/delete_user.html'
    success_url = reverse_lazy('homepage')

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'delete_content' in request.POST:
            Book.objects.filter(created_by=self.object).delete()
            Review.objects.filter(user=self.object).delete()
        self.object.delete()


class PasswordChangeView(auth_mixins.LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'user_templates/password_change.html'
    form_class = auth_forms.PasswordChangeForm
    success_url = reverse_lazy('password_changed')


class PasswordChangedView(auth_mixins.LoginRequiredMixin, TemplateView):
    template_name = 'user_templates/password_changed.html'


class ShelfView(auth_mixins.LoginRequiredMixin, ListView):
    model = Shelf
    template_name = 'shelf_templates/user_shelf.html'
