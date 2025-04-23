from django.http import HttpResponseForbidden
from django.shortcuts import reverse, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied

from redis.commands.search.querystring import querystring

from reviews.models import Review
from reviews.forms import ReviewForm
from users.models import User


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


class ReviewCreateView(CreateView):
    ...


class ReviewDetailView(DetailView):
    ...

class ReviewUpdateView(UpdateView):
    ...

class ReviewDeleteView(DeleteView):
    ...
