from django.urls import path

from reviews.apps import ReviewsConfig
from reviews.views import (ReviewListView, ReviewDeactivatedListView, ReviewCreateView, ReviewDetailView,
                           ReviewUpdateView, ReviewDeleteView)

app_name = ReviewsConfig.name

urlpatterns = [
    path('', ReviewListView.as_view(), name='reviews_list'),
    path('deactivated/', ReviewDeactivatedListView.as_view(), name='reviews_deactivated'),
    path('review/create/', ReviewCreateView.as_view(), name='reviews_deactivated'),
    path('review/create/', ReviewCreateView.as_view(), name='reviews_deactivated'),
    path('review/create/', ReviewCreateView.as_view(), name='reviews_deactivated'),
]