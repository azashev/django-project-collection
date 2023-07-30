from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import DetailView, FormView, DeleteView, TemplateView
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
            Shelf.objects.create(user=user)
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
        Book.objects.filter(created_by=self.object).delete()
        Review.objects.filter(user=self.object).delete()
        self.object.delete()
        return redirect(self.success_url)


class PasswordChangeView(auth_mixins.LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'user_templates/password_change.html'
    form_class = auth_forms.PasswordChangeForm

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Password changed successfully!")

        return response

    def get_success_url(self):
        return reverse('update_profile')


class ShelfView(auth_mixins.LoginRequiredMixin, DetailView):
    model = Shelf
    template_name = 'user_templates/user_shelf.html'

    def get_object(self, queryset=None):
        return self.request.user.shelf


class AddToShelfView(auth_mixins.LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book, id=kwargs['pk'])
        shelf, created = Shelf.objects.get_or_create(user=request.user)
        if shelf.books.count() >= 5:
            messages.error(request, "You cannot have more than 5 books in your shelf!")
            return redirect('book_details', pk=book.pk)
        shelf.books.add(book)
        messages.success(request, "Successfully added a book to the shelf!")
        return redirect('book_details', pk=book.pk)


class RemoveFromShelfView(auth_mixins.LoginRequiredMixin, DeleteView):
    template_name = 'user_templates/delete_book_from_shelf.html'

    def get_object(self, queryset=None):
        shelf = get_object_or_404(Shelf, user=self.request.user)
        book = get_object_or_404(Book, pk=self.kwargs.get('pk'))

        if book not in shelf.books.all():
            raise Http404("Book not found on your shelf")

        return book

    def get_success_url(self):
        return reverse('shelf')


class ProfileBooksView(auth_mixins.LoginRequiredMixin, View):
    template_name = 'user_templates/my_books.html'

    def get(self, request, *args, **kwargs):
        books = Book.objects.filter(created_by=self.request.user)
        books_with_genres = []

        for book in books:
            book_genres = ", ".join([genre.genre_name for genre in book.genres.all()])
            books_with_genres.append({
                'title': book.title,
                'image': book.book_image,
                'description': book.description,
                'genres': book_genres,
                'author': book.author,
                'pk': book.pk,
            })

        context = {
            'books': books_with_genres,
        }

        return render(request, self.template_name, context)
