# coding: utf-8

from django.views import generic
from harvest.models import Harvest, Property, Equipment, \
    RequestForParticipation, TreeType, Comment
from harvest.forms import CommentForm, RequestForm, HarvestForm
from member.models import Person, AuthUser, Actor, Address
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from filters import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from dal import autocomplete
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


class PropertyList(generic.ListView):
    template_name = 'harvest/properties/list.html'
    context_object_name = 'properties'
    model = Property

    def dispatch(self, *args, **kwargs):
        return super(PropertyList, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PropertyList, self).get_context_data(**kwargs)
        context['view'] = "properties"

        return context


class PropertyDetail(generic.DetailView):
    model = Property
    context_object_name = 'property'
    template_name = 'harvest/properties/detail.html'

    def dispatch(self, *args, **kwargs):
        get_object_or_404(
            Property,
            id=self.kwargs['pk']
        )

        return super(PropertyDetail, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PropertyDetail, self).get_context_data(**kwargs)
        property_history = Property.history.filter(id=self.kwargs['pk'])
        context['property_history'] = property_history

        return context


class PropertyCreate(generic.CreateView):
    model = Property
    template_name = 'harvest/properties/create.html'
    fields = '__all__'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PropertyCreate, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return self.object.get_absolute_url()


class PropertyUpdate(generic.UpdateView):
    model = Property
    template_name = "harvest/properties/update.html"
    fields = '__all__'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        property = get_object_or_404(
            Property,
            id=kwargs['pk']
        )
        return super(PropertyUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'harvest:property_detail',
            kwargs={'pk': self.kwargs['pk']}
        )


class HarvestList(generic.ListView):
    template_name = 'harvest/harvest/list.html'
    context_object_name = 'harvests'
    model = Harvest

    def dispatch(self, *args, **kwargs):
        return super(HarvestList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return HarvestFilter(self.request.GET, queryset=Harvest.objects.all())

    def get_context_data(self, **kwargs):
        context = super(HarvestList, self).get_context_data(**kwargs)

        all_harvests = HarvestFilter(self.request.GET, queryset=Harvest.objects.all())
        context['view'] = "harvests"
        context['form'] = all_harvests.form

        return context


class HarvestDetail(generic.DetailView):
    model = Harvest
    context_object_name = 'harvest'
    template_name = 'harvest/harvest/detail_public.html'

    def dispatch(self, *args, **kwargs):
        get_object_or_404(
            Harvest,
            id=self.kwargs['pk']
        )
        if self.request.user.is_authenticated():
            self.template_name = 'harvest/harvest/detail.html'

        return super(HarvestDetail, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HarvestDetail, self).get_context_data(**kwargs)

        harvest_history = Harvest.history.filter(id=self.kwargs['pk'])
        context['harvest_history'] = harvest_history
        context['form_comment'] = CommentForm()
        context['form_request'] = RequestForm()

        return context


class HarvestCreate(generic.CreateView):
    model = Harvest
    template_name = 'harvest/harvest/create.html'
    form_class = HarvestForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HarvestCreate, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return self.object.get_absolute_url()


class HarvestUpdate(generic.UpdateView):
    model = Harvest
    template_name = "harvest/harvest/update.html"
    fields = '__all__'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        harvest = get_object_or_404(
            Harvest,
            id=kwargs['pk']
        )
        return super(HarvestUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'harvest:harvest_detail',
            kwargs={'pk': self.kwargs['pk']}
        )


class EquipmentList(generic.ListView):
    template_name = 'harvest/equipment/list.html'
    context_object_name = 'equipments'
    model = Equipment

    def dispatch(self, *args, **kwargs):
        return super(EquipmentList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Equipment.objects.all()


class EquipmentCreate(generic.CreateView):
    model = Equipment
    template_name = 'harvest/equipment/create.html'
    fields = '__all__'

    def dispatch(self, *args, **kwargs):
        return super(EquipmentCreate, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return self.object.get_absolute_url()


class RequestForParticipationCreate(generic.CreateView):
    model = RequestForParticipation
    template_name = 'harvest/participation/create.html'
    form_class = RequestForm

    def dispatch(self, *args, **kwargs):
        return super(RequestForParticipationCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.harvest = Harvest.objects.get(id=self.kwargs['pk'])
        return super(RequestForParticipationCreate, self).form_valid(form)

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Your request of participation has been send. The pickleader will contact you soon!')
        )
        return reverse_lazy(
            'harvest:harvest_detail',
            kwargs={'pk': self.kwargs['pk']}
        )


class CommentCreate(generic.CreateView):
    model = Comment
    template_name = 'harvest/harvest/create_comment.html'
    fields = [
        'content'
    ]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CommentCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.harvest = Harvest.objects.get(id=self.kwargs['pk'])
        return super(CommentCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'harvest:harvest_detail',
            kwargs={'pk': self.kwargs['pk']}
        )


class PickLeaderAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Person.objects.none()

        qs = AuthUser.objects.filter(is_staff=True)

        if self.q:
            qs = qs.filter(person__first_name__istartswith=self.q)

        return qs

class PersonAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Person.objects.none()

        qs = Person.objects.all()

        if self.q:
            qs = qs.filter(first_name__istartswith=self.q)

        return qs


class ActorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Actor.objects.none()

        qs = Actor.objects.all()
        list_actor = []

        if self.q:
            first_name = qs.filter(person__first_name__icontains=self.q)
            family_name = qs.filter(person__family_name__icontains=self.q)

            for actor in first_name:
                if actor not in list_actor:
                    list_actor.append(actor)

            for actor in family_name:
                if actor not in list_actor:
                    list_actor.append(actor)

        return list_actor


class TreeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return TreeType.objects.none()

        qs = TreeType.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class PropertyAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Property.objects.none()

        qs = Property.objects.all()
        list_property = []

        if self.q:
            number = qs.filter(address__number__icontains=self.q)
            street = qs.filter(address__street__icontains=self.q)
            city = qs.filter(address__city__name__icontains=self.q)
            postal_code = qs.filter(address__postal_code__icontains=self.q)
            first_name = qs.filter(owner__person__first_name__icontains=self.q)
            family_name = qs.filter(owner__person__family_name__icontains=self.q)

            for actor in first_name:
                if actor not in list_property:
                    list_property.append(actor)

            for actor in family_name:
                if actor not in list_property:
                    list_property.append(actor)

            for address in postal_code:
                if address not in list_property:
                    list_property.append(address)

            for address in number:
                if address not in list_property:
                    list_property.append(address)

            for address in street:
                if address not in list_property:
                    list_property.append(address)

            for address in city:
                if address not in list_property:
                    list_property.append(address)

        return list_property


class EquipmentAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Equipment.objects.none()

        qs = Equipment.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class AddressAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Address.objects.none()

        qs = Address.objects.all()
        list_address = []

        if self.q:
            number = qs.filter(number__icontains=self.q)
            street = qs.filter(street__icontains=self.q)
            city = qs.filter(city__name__icontains=self.q)
            postal_code = qs.filter(postal_code__icontains=self.q)

            for address in postal_code:
                if address not in list_address:
                    list_address.append(address)

            for address in number:
                if address not in list_address:
                    list_address.append(address)

            for address in street:
                if address not in list_address:
                    list_address.append(address)

            for address in city:
                if address not in list_address:
                    list_address.append(address)

        return list_address
