from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from dogs.models import Breed, Dog
from dogs.forms import DogForm


def index(request):
    context = {
        'objects_list': Breed.objects.all()[:3],
        'title': 'Питомник - Главная'
    }
    return render(request, 'dogs/index.html', context)


def breeds_list_view(request):
    context = {
        'objects_list': Breed.objects.all(),
        'title': 'Питомник - Все наши породы'
    }
    return render(request, 'dogs/breeds.html', context)


def breed_dogs_list_view(request, pk):
    breed_item = Breed.objects.get(pk=pk)
    context = {
        'objects_list': Dog.objects.filter(breed_id=pk),
        'title': f'Собаки породы - {breed_item.name}',
        'breed_pk': breed_item.pk
    }
    return render(request, 'dogs/dogs.html', context)

def dogs_list_view(request):
    context = {
        'objects_list': Dog.objects.all(),
        'title': 'Питомник - Все наши собаки'
    }
    return render(request, 'dogs/dogs.html', context)


@login_required
def dog_create_view(request):
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            dog_object = form.save(commit=False)
            dog_object.owner = request.user
            dog_object.save()
            return HttpResponseRedirect(reverse('dogs:dogs_list'))
    return render(request, 'dogs/create_update.html', {'form': DogForm()})


@login_required
def dog_detail_view(request, pk):
    dog_object = Dog.objects.get(pk=pk)
    context = {
        'object': dog_object,
        'title': f'Вы выбрали {dog_object.name}. Порода: {dog_object.breed.name}'
    }
    return render(request, 'dogs/detail.html', context)


@login_required
def dog_update_view(request, pk):
    dog_object = get_object_or_404(Dog, pk=pk)
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES, instance=dog_object)
        if form.is_valid():
            dog_object = form.save(commit=False)
            dog_object.save()
            return HttpResponseRedirect(reverse('dogs:dog_detail', args={pk: pk})) # удивительно, но надо передавать args именно так
    context = {
        'object': dog_object,
        'form': DogForm(instance=dog_object)
    }
    return render(request, 'dogs/create_update.html', context)


@login_required
def dog_delete_view(request, pk):
    dog_object = get_object_or_404(Dog, pk=pk)
    if request.method == 'POST':
        dog_object.delete()
        return HttpResponseRedirect(reverse('dogs:dogs_list'))
    context = {
        'object': dog_object
    }
    return render(request, 'dogs/delete.html', context)