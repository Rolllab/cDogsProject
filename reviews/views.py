from django.http import HttpResponseForbidden
from django.shortcuts import reverse, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied

from redis.commands.search.querystring import querystring

from reviews.models import Review
from reviews.forms import ReviewForm
from users.models import User, UserRoles
from reviews.utils import slug_generator


class ReviewListView(ListView):
    model = Review
    template_name = 'reviews/reviews.html'
    extra_context = {
        'title': 'Все отзывы'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(sign_of_review=True)
        return queryset


class ReviewDeactivatedListView(ListView):
    model = Review
    template_name = 'reviews/reviews.html'
    extra_context = {
        'title': 'Не активные отзывы'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(sign_of_review=False)
        return queryset


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/create_update.html'
    extra_context = {
        'title': 'Написать отзыв'
    }

    def form_valid(self, form):
        # UserRoles.ADMIN использовать только при разработке, потом удалить
        if self.request.user.role not in [UserRoles.USER, UserRoles.ADMIN]:
            return HttpResponseForbidden
        self.object = form.save()
        if self.object.slug == 'temp_slug':
            self.object.slug = slug_generator()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class ReviewDetailView(LoginRequiredMixin, DetailView):
    model = Review
    template_name = 'reviews/detail.html'
    extra_context = {
        'title': 'Просмотр отзыва'
    }

class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/create_update.html'
    extra_context = {
        'title': 'Изменить отзыв'
    }

    def get_success_url(self):
        return reverse('reviews:review_detail', args=[self.kwargs.get('slug')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset=queryset)
        if self.object.author != self.request.user and self.request.user not in [UserRoles.ADMIN, UserRoles.MODERATOR]:
            raise PermissionDenied()
        return self.object


class ReviewDeleteView(PermissionRequiredMixin, DeleteView):
    model = Review
    template_name = 'reviews/delete.html'
    permission_required = 'reviews.delete_review'

    def has_permission(self):
        # Стандартная проверка прав
        has_perm = super().has_permission()
        # Дополнительная проверка: разрешить автору удалять свой отзыв
        review = self.get_object()
        return has_perm or review.author == self.request.user

    def get_success_url(self):
        return reverse('reviews:reviews_list')


def review_toggle_activity(request, slug):
    review_item = get_object_or_404(Review, slug=slug)
    if review_item.sign_of_review:
        review_item.sign_of_review = False
        review_item.save()
        return redirect(reverse('reviews:reviews_deactivated'))
    else:
        review_item.sign_of_review = True
        review_item.save()
        return redirect(reverse('reviews:reviews_list'))
