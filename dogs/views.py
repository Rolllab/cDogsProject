from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.forms import inlineformset_factory
from django.core.exceptions import PermissionDenied

from dogs.models import Breed, Dog, DogParent
from dogs.forms import DogForm, DogParentForm
from users.models import UserRoles


def index(request):
    context = {
        'object_list': Breed.objects.all()[:3],
        'title': 'Питомник - Главная'
    }
    return render(request, 'dogs/index.html', context)


class BreedsListView(LoginRequiredMixin, ListView):
    model = Breed
    template_name = 'dogs/breeds.html'
    extra_context = {
        'title': 'Все наши породы'
    }
# def breeds_list_view(request):
#     context = {
#         'object_list': Breed.objects.all(),
#         'title': 'Питомник - Все наши породы'
#     }
#     return render(request, 'dogs/breeds.html', context)


class DogBreedListView(LoginRequiredMixin, ListView):
    model = Dog
    template_name = 'dogs/dogs.html'
    extra_context = {
        'title': 'Собаки выбранной породы'
    }

    def get_queryset(self):
        queryset = super().get_queryset().filter(breed_id=self.kwargs.get('pk'))
        return queryset


class DogListView(ListView):
    model = Dog
    extra_context = {
        'title': 'Питомник - Все наши собаки'
    }
    template_name = 'dogs/dogs.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset


class DogDeactivatedListView(LoginRequiredMixin, ListView):
    model = Dog
    template_name = 'dogs/dogs.html'
    extra_context = {
        'title': 'Питомник - не активные собаки'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role in [UserRoles.MODERATOR, UserRoles.ADMIN]:
            queryset = queryset.filter(is_active=False)
        if self.request.user.role == UserRoles.USER:
            queryset = queryset.filter(is_active=False, owner=self.request.user)
        return queryset


class DogCreateView(LoginRequiredMixin, CreateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'
    extra_context = {
        'title': 'Питомник - Все наши собаки'
    }
    success_url = reverse_lazy('dogs:dogs_list')

    # Привязка к аккаунту. Тот, кто создал - тот и будет хозяином
    def form_valid(self, form):
        if self.request.user.role != UserRoles.USER:
            raise PermissionDenied

        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class DogDetailView(DetailView):
    model = Dog
    template_name = 'dogs/detail.html'

    # Вместо extra_context
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Подробная информация {self.object}'
        return context_data


class DogUpdateView(LoginRequiredMixin, UpdateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'
    extra_context = {
        'title': 'Изменить собаку'
    }

    def get_success_url(self):
        return reverse('dogs:dog_detail', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        # if self.object.owner != self.request.user and not self.request.user.is_staff:
        # Разрешение на редактирование карточки только владельцам
        if self.object.owner != self.request.user and self.request.user.role != UserRoles.ADMIN:
            raise PermissionDenied
        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        DogParentFormset = inlineformset_factory(Dog, DogParent, form=DogParentForm, extra=1)
        if self.request.method == 'POST':
            formset = DogParentFormset(self.request.POST, instance=self.object)
        else:
            formset = DogParentFormset(instance=self.object)
        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        
        return super().form_valid(form) 

class DogDeleteView(PermissionRequiredMixin, DeleteView):
    model = Dog
    template_name = 'dogs/delete.html'
    extra_context = {
        'title': 'Удалить собаку'
    }
    success_url = reverse_lazy('dogs:dogs_list')
    permission_required = 'dogs.delete_dog'
    permission_denied_message = 'У вас нет нужных прав для этого действия'


def dog_toggle_activity(request, pk):
    dog_item = get_object_or_404(Dog, pk=pk)
    if dog_item.is_active:
        dog_item.is_active = False
    else:
        dog_item.is_active = True
    dog_item.save()
    return redirect(reverse('dogs:dogs_list'))
