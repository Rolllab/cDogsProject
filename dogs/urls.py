from django.urls import path

from dogs.views import index, DogBreedListView, BreedsListView, DogListView, DogCreateView, DogDeleteView, \
    DogDetailView, DogUpdateView, DogDeactivatedListView, dog_toggle_activity, DogSearchListView, BreedsSearchListView
from dogs.apps import DogsConfig
from django.views.decorators.cache import cache_page, never_cache


app_name = DogsConfig.name

urlpatterns = [
    path('', cache_page(60)(index), name='index'),
    path('breeds/', cache_page(60)(BreedsListView.as_view()), name='breeds'),
    path('breeds/<int:pk>/dogs/', DogBreedListView.as_view(), name='breed_dogs'),
    path('breeds/search/', BreedsSearchListView.as_view(), name='breeds_search'),

    path('dogs/', DogListView.as_view(), name='dogs_list'),
    path('dogs/deactivate/', DogDeactivatedListView.as_view(), name='dogs_deactivated_list'),
    path('dogs/search/', DogSearchListView.as_view(), name='dogs_search'),
    path('dogs/create/', DogCreateView.as_view(), name='dog_create'),
    path('dogs/detail/<int:pk>/', DogDetailView.as_view(), name='dog_detail'),
    path('dogs/update/<int:pk>/', never_cache(DogUpdateView.as_view()), name='dog_update'),
    path('dogs/toggle/<int:pk>/', dog_toggle_activity, name='dog_toggle_activity'),
    path('dogs/delete/<int:pk>/', DogDeleteView.as_view(), name='dog_delete'),
]