# coding: utf-8

from django.views import generic
from django.http import JsonResponse
from harvest.models import Harvest, Property, Equipment, \
    RequestForParticipation
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from filters import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse


class Calendar(generic.TemplateView):
    template_name = 'harvest/calendar.html'

    def dispatch(self, request, *args, **kwargs):
        return super(Calendar, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Calendar, self).get_context_data(**kwargs)

        context['view'] = "calendar"

        return context


class JsonCalendar(generic.View):
    def get(self, test):
        harvests = Harvest.objects.filter(is_active=True)
        event = {}
        events = []
        for harvest in harvests:
            event["title"] = harvest.property.address.neighborhood.name
            event["allday"] = "false"
            event["description"] = harvest.about
            event["start"] = harvest.start_date
            event["end"] = harvest.end_date
            event["url"] = reverse(
                'harvest:harvest_detail',
                kwargs={'pk': harvest.id}
            )
            events.append(event)

        print events
        return JsonResponse(events, safe=False)


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
    template_name = 'harvest/harvest/detail.html'

    def dispatch(self, *args, **kwargs):
        get_object_or_404(
            Property,
            id=self.kwargs['pk']
        )

        return super(HarvestDetail, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HarvestDetail, self).get_context_data(**kwargs)

        harvest_history = Harvest.history.filter(id=self.kwargs['pk'])
        context['harvest_history'] = harvest_history

        return context


class HarvestCreate(generic.CreateView):
    model = Harvest
    template_name = 'harvest/harvest/create.html'
    fields = '__all__'

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
    fields = [
        'first_time_picker',
        'helper_picker',
    ]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RequestForParticipationCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.harvest = Harvest.objects.get(id=self.kwargs['pk'])
        form.instance.picker = self.request.user
        return super(RequestForParticipationCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'harvest:harvest_detail',
            kwargs={'pk': self.kwargs['pk']}
        )