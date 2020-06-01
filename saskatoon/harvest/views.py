# coding: utf-8
from django.views import generic
from harvest.models import Harvest, Property, Equipment, \
    RequestForParticipation, TreeType, Comment, \
    PropertyImage, HarvestYield, HarvestImage
from harvest.forms import HarvestYieldForm, CommentForm, RequestForm, PropertyForm, PublicPropertyForm, \
    HarvestForm, PropertyImageForm, EquipmentForm, RFPManageForm, HarvestYieldForm
from member.models import Person, AuthUser, Actor, Organization, Neighborhood
from harvest.filters import HarvestFilter, PropertyFilter
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from dal import autocomplete
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from django.db.models import Sum, Count, Q


class OrganizationList(generic.ListView):
    template_name = 'harvest/organizations/list.html'
    context_object_name = 'organizations'
    model = Organization

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(OrganizationList, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OrganizationList, self).get_context_data(**kwargs)
        organizations = Organization.objects.filter(is_beneficiary=True)
        context['view'] = organizations
        context['organizations'] = organizations

        return context

class PropertyList(generic.ListView):
    template_name = 'harvest/properties/list.html'
    context_object_name = 'properties'
    model = Property

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PropertyList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        request = self.request.GET
        queryset = Property.objects.all().order_by('-id')
        return PropertyFilter(
            request,
            queryset
        )

    def get_context_data(self, **kwargs):
        context = super(PropertyList, self).get_context_data(**kwargs)
        request = self.request.GET.copy()
        queryset = Property.objects.all().order_by('-id')
        active_properties = Property.objects.filter(authorized=True)
        all_properties = PropertyFilter(
            request,
            queryset
        )
        context['view'] = "properties"
        context['active_properties'] = active_properties
        context['form'] = all_properties.form

        return context


class PropertyDetail(generic.DetailView):
    model = Property
    context_object_name = 'property'
    template_name = 'harvest/properties/detail.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        get_object_or_404(
            Property,
            id=self.kwargs['pk']
        )

        return super(PropertyDetail, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PropertyDetail, self).get_context_data(**kwargs)
        context['form_image'] = PropertyImageForm()

        return context

class PropertyCreate(generic.CreateView):
    model = Property
    template_name = 'harvest/properties/create.html'
    form_class = PropertyForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PropertyCreate, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return self.object.get_absolute_url()

class PublicPropertyCreate(generic.CreateView):
    model = Property
    template_name = 'harvest/properties/create.html'
    form_class = PublicPropertyForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PublicPropertyCreate, self).dispatch(*args, **kwargs)

    def get_success_url(self):
            return reverse_lazy(
                #'harvest:equipment_list'
                'harvest:property_thanks'
            )

class PropertyThanks(generic.TemplateView):
    template_name =  'harvest/properties/thanks.html'
    def get_context_data(self, **kwargs):
        context = super(PropertyThanks, self).get_context_data(**kwargs)
        return context

class PropertyUpdate(generic.UpdateView):
    model = Property
    template_name = "harvest/properties/create.html"
    form_class = PropertyForm

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


class PropertyImageCreate(generic.CreateView):
    model = PropertyImage
    template_name = 'harvest/properties/add_image.html'
    fields = [
        'image'
    ]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PropertyImageCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.property = Property.objects.get(id=self.kwargs['pk'])
        return super(PropertyImageCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'harvest:property_detail',
            kwargs={'pk': self.kwargs['pk']}
        )


class HarvestImageCreate(generic.CreateView):
    model = HarvestImage
    template_name = 'harvest/harvests/add_image.html'
    fields = [
        'image'
    ]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HarvestImageCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.harvest = Harvest.objects.get(id=self.kwargs['pk'])
        return super(HarvestImageCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'harvest:harvest_detail',
            kwargs={'pk': self.kwargs['pk']}
        )


class HarvestList(generic.ListView):
    template_name = 'harvest/harvest/list.html'
    context_object_name = 'harvests'
    model = Harvest

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HarvestList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        request = self.request.GET
        queryset=Harvest.objects.all().order_by('-id')
        return HarvestFilter(
            request,
            queryset
        )

    def get_context_data(self, **kwargs):
        context = super(HarvestList, self).get_context_data(**kwargs)
        request = self.request.GET.copy()
        queryset=Harvest.objects.all().order_by('-id')
        if 'start_date' not in request:
            import time
            current_year = time.strftime("%Y")
            request['start_date'] = current_year
        all_harvests = HarvestFilter(
            request,
            queryset
        )
        context['view'] = "harvests"
        context['all_harvests'] = all_harvests
        context['form'] = all_harvests.form

        return context


class HarvestDetail(generic.DetailView):
    model = Harvest
    context_object_name = 'harvest'
    template_name = 'harvest/harvest/detail.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        get_object_or_404(
            Harvest,
            id=self.kwargs['pk']
        )

        return super(HarvestDetail, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HarvestDetail, self).get_context_data(**kwargs)

        harvest = Harvest.objects.get(id=self.kwargs['pk'])
        requests = RequestForParticipation.objects.filter(harvest=harvest)
        distribution = HarvestYield.objects.filter(harvest=harvest)

        context['form_comment'] = CommentForm()
        context['form_request'] = RequestForm()
        context['form_manage_request'] = RFPManageForm()
        context['requests'] = requests
        context['distribution'] = distribution
        context['form_edit_recipient'] = HarvestYieldForm()

        return context


class HarvestCreate(generic.CreateView):
    model = Harvest
    template_name = 'harvest/harvest/create.html'
    form_class = HarvestForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HarvestCreate, self).dispatch(*args, **kwargs)

    def get_initial(self):
        initial_data = {}

        if 'property' in self.kwargs:
            initial_data['property'] = self.kwargs['property']

        return initial_data

    def get_success_url(self):
        return self.object.get_absolute_url()


class HarvestUpdate(generic.UpdateView):
    model = Harvest
    template_name = "harvest/harvest/create.html"
    form_class = HarvestForm

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


class HarvestAdopt(generic.RedirectView):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.harvest = get_object_or_404(
            Harvest,
            id=kwargs['pk']
        )
        is_staff = request.user.is_staff

        if is_staff:
            return super(HarvestAdopt, self).\
                dispatch(request, *args, **kwargs)
        else:
            messages.add_message(
                request,
                messages.ERROR,
                _("You do not have the right permissions")
            )
            return redirect(reverse_lazy(
                "harvest:harvest_detail",
                args=[self.harvest.id]
            ))

    def get(self, request, *args, **kwargs):
        self.harvest.pick_leader = request.user
        self.harvest.status = "Adopted"
        self.harvest.save(update_fields=['pick_leader', 'status'])

        messages.add_message(
            request,
            messages.WARNING,
            _('Thanks, you adopted this harvest!')
        )

        return redirect(self.get_redirect_url(*args, **kwargs))

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy(
            "harvest:harvest_detail",
            args=[self.harvest.id]
        )


class RequestForParticipationUpdate(generic.UpdateView):
    model = RequestForParticipation
    context_object_name = 'participation'
    template_name = "harvest/participation/update.html"
    form_class = RFPManageForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        participation = get_object_or_404(
            RequestForParticipation,
            id=kwargs['pk']
        )
        return super(RequestForParticipationUpdate, self).\
            dispatch(request, *args, **kwargs)

    def get_success_url(self):
        request = RequestForParticipation.objects.get(id=self.kwargs['pk'])
        return reverse_lazy(
            'harvest:harvest_detail',
            kwargs={'pk': request.harvest.id}
        )


    def get_context_data(self, **kwargs):
        context = super(RequestForParticipationUpdate, self).\
            get_context_data(**kwargs)
    
        participation = RequestForParticipation.objects.get(id=self.kwargs['pk'])
    
        context['participation'] = participation
    
        return context
    

class EquipmentList(generic.ListView):
    template_name = 'harvest/equipment/list.html'
    context_object_name = 'equipments'
    model = Equipment

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EquipmentList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Equipment.objects.all()


class ParticipationList(generic.ListView):
    template_name = 'harvest/participation/list.html'
    context_object_name = 'participations'
    model = RequestForParticipation

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ParticipationList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return RequestForParticipation.objects.all()


class EquipmentCreate(generic.CreateView):
    model = Equipment
    template_name = 'harvest/equipment/create.html'
    form_class = EquipmentForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EquipmentCreate, self).dispatch(*args, **kwargs)

    def get_initial(self):
        initial_data = {}

        if 'property' in self.kwargs:
            initial_data['property'] = self.kwargs['property']

        return initial_data

    def get_success_url(self):
        if self.object.property:
            return self.object.property.get_absolute_url()
        else:
            return reverse_lazy(
                'harvest:equipment_list'
            )


class RequestForParticipationCreate(generic.CreateView):
    model = RequestForParticipation
    template_name = 'harvest/participation/create.html'
    form_class = RequestForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RequestForParticipationCreate, self).\
            dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.harvest = Harvest.objects.get(id=self.kwargs['pk'])
        return super(RequestForParticipationCreate, self).form_valid(form)

    def get_initial(self):
        initial = super(RequestForParticipationCreate, self).get_initial()
        initial['harvest_id'] = self.kwargs['pk']
        return initial

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Your request of participation has been sent. '
              'The pick leader will contact you soon!')
        )
        if not self.request.user.is_authenticated():
            return reverse_lazy('app:calendar')
        else:
            return reverse_lazy(
                'harvest:harvest_detail',
                kwargs={'pk': self.kwargs['pk']}
            )



class HarvestYieldCreate(generic.CreateView):
    model = HarvestYield
    template_name = 'harvest/harvest_yield/create.html'
    fields = [
        'tree',
        'total_in_lb',
        'recipient',
    ]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HarvestYieldCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.harvest = Harvest.objects.get(id=self.kwargs['pk'])
        return super(HarvestYieldCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(HarvestYieldCreate, self).get_context_data(**kwargs)

        trees = Harvest.objects.get(id=self.kwargs['pk']).trees.all()
        model_choice_tree = forms.ModelChoiceField(
            queryset=trees,
            required=False
        )
        context['form'].fields['tree'] = model_choice_tree

        harvest = Harvest.objects.get(id=self.kwargs['pk'])
        requests = harvest.request_for_participation.filter(
            is_accepted=True
        )
        pickers = []
        for request_participation in requests:
            pickers.append(request_participation.picker)

        organizations = Organization.objects.filter(is_beneficiary=True)
        owner = harvest.property.owner

        recipients = set()
        recipients.add(owner.actor_id)
        if harvest.pick_leader:
            recipients.add(harvest.pick_leader.person.actor_id)
        for organization in organizations:
            recipients.add(organization.pk)
        for picker in pickers:
            recipients.add(picker.pk)

        recipients = Actor.objects.filter(pk__in=recipients)

        model_choice_recipient = forms.ModelChoiceField(
            queryset=recipients,
            required=False
        )
        context['form'].fields['recipient'] = model_choice_recipient

        return context

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Your recipient has been added!')
        )
        return reverse_lazy(
            'harvest:harvest_detail',
            kwargs={'pk': self.kwargs['pk']}
        )


class HarvestYieldUpdate(generic.UpdateView):
    model = HarvestYield
    template_name = 'harvest/harvest_yield/update.html'
    fields = [
        'tree',
        'total_in_lb',
        'recipient',
    ]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HarvestYieldUpdate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        harvest = HarvestYield.objects.get(id=self.kwargs['pk']).harvest
        form.instance.harvest = Harvest.objects.get(id=harvest.id)
        self.kwargs['pk'] = harvest.id #not sure why we needed it
        return super(HarvestYieldUpdate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(HarvestYieldUpdate, self).get_context_data(**kwargs)

        harvest = HarvestYield.objects.get(id=self.kwargs['pk']).harvest

        trees = Harvest.objects.get(id=harvest.id).trees.all()
        model_choice_tree = forms.ModelChoiceField(
            queryset=trees,
            required=False
        )
        context['form'].fields['tree'] = model_choice_tree

        harvest = Harvest.objects.get(id=harvest.id)
        requests = harvest.request_for_participation.filter(
            is_accepted=True
        )
        pickers = []
        for request_participation in requests:
            pickers.append(request_participation.picker)

        organizations = Organization.objects.filter(
            is_beneficiary=True
        )
        owner = harvest.property.owner

        recipients = set()
        recipients.add(owner.actor_id)
        if harvest.pick_leader:
            recipients.add(harvest.pick_leader.person.actor_id)
        for organization in organizations:
            recipients.add(organization.pk)
        for picker in pickers:
            recipients.add(picker.pk)

        recipients = Actor.objects.filter(pk__in=recipients)

        model_choice_recipient = forms.ModelChoiceField(
            queryset=recipients,
            required=False
        )
        context['form'].fields['recipient'] = model_choice_recipient
        context['harvest'] = harvest

        return context

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Your recipient has been updated!')
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

    def get_initial(self):
        initial = super(CommentCreate, self).get_initial()
        initial['harvest_id'] = self.kwargs['pk']
        return initial


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
            qs = qs.filter(first_name__icontains=self.q)

        return qs


class ActorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Actor.objects.none()

        qs = Actor.objects.all()
        list_actor = []

        if self.q:
            first_name = qs.filter(
                person__first_name__icontains=self.q
            )
            family_name = qs.filter(
                person__family_name__icontains=self.q
            )
            civil_name = qs.filter(
                organization__civil_name__icontains=self.q
            )

            for actor in first_name:
                if actor not in list_actor:
                    list_actor.append(actor)

            for actor in family_name:
                if actor not in list_actor:
                    list_actor.append(actor)

            for actor in civil_name:
                if actor not in list_actor:
                    list_actor.append(actor)

        if not list_actor:
            list_actor = qs

        return list_actor


class TreeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = TreeType.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

class PropertyAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Property.objects.none()

        qs = Property.objects.all()

        if self.q:
             qs = Property.objects.filter(Q(owner__person__first_name__icontains=self.q) | Q(owner__person__family_name__icontains=self.q))

        return qs


class EquipmentAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Equipment.objects.none()

        qs = Equipment.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

class Stats(generic.ListView):
    template_name = 'harvest/stats/stats.html'
    context_object_name = 'stats'
    model = Harvest

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Stats, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Stats, self).get_context_data(**kwargs)
        season = self.kwargs['season']
        context['view'] = "stats"
        context['seasons'] = self.get_seasons()
        context['season'] = self.kwargs['season']
        print self.get_seasons()
        context['data2'] = self.barchart()
        context['total_fruit'] = self.get_total_weight_per_fruit(season)
        context['total_beneficiary'] = self.get_total_weight_per_beneficiary(season)
        context['total_picker'] = self.get_total_weight_per_picker(season)
        context['total_neighborhood'] = self.get_total_weight_per_neighborhood(season)

        # Highlights
        context['highlights'] = self.get_highlights(season)
        
        return context

    def get_seasons(self):
        seasons = []
        for y in Harvest.objects.all():
            if y.start_date is not None:
                seasons.append(y.start_date.strftime("%Y"))
        seasons = list(set(seasons))
        return seasons 

    def get_highlights(self, season):
        s = season
        h = {}
        if s == "all":
            h["total_weight"] = int(HarvestYield.objects.filter(harvest__status="Succeeded").aggregate(Sum('total_in_lb')).get('total_in_lb__sum'))
            h["total_harvests"] = Harvest.objects.filter(status="Succeeded").count()
            h["total_pickers"] = HarvestYield.objects.filter(harvest__status="Succeeded").values('recipient').distinct().count()
        else:
            h["total_weight"] = int(HarvestYield.objects.filter(harvest__status="Succeeded").filter(harvest__start_date__year=s).aggregate(Sum('total_in_lb')).get('total_in_lb__sum'))
            h["total_harvests"] = Harvest.objects.filter(status="Succeeded").filter(start_date__year=s).count()
            h["total_pickers"] = HarvestYield.objects.filter(harvest__status="Succeeded").filter(harvest__start_date__year=s).values('recipient').distinct().count()

        beneficiaries = Organization.objects.all()
        b_list = []
        for beneficiary in beneficiaries:
            if season == 'all':
                total = HarvestYield.objects.filter(harvest__status="Succeeded").filter(recipient=beneficiary).aggregate(Sum('total_in_lb'))
            else:
                total = HarvestYield.objects.filter(harvest__status="Succeeded").filter(recipient=beneficiary).filter(harvest__start_date__year=season).aggregate(Sum('total_in_lb'))
            # If beneficiary got some fruit
            if total.get('total_in_lb__sum') is not None:
                b_list.append(beneficiary) 
        h["total_beneficiary"] = len(b_list)

        return h

    def get_total_weight_list_all_seasons(self):
        seasons = self.get_seasons()
        total_list = []
        for s in seasons:
            total = HarvestYield.objects.filter(harvest__status="Succeeded").filter(harvest__start_date__year=s).aggregate(Sum('total_in_lb'))
            total_times = Harvest.objects.filter(status="Succeeded").filter(harvest__start_date__year=s).count()
            total_list.append((s, total_times, total.get('total_in_lb__sum')))
        return total_list


    def get_total_weight_per_fruit(self, season):
        tt = TreeType.objects.all().order_by('fruit_name')
        total_list = []
        for t in tt:
            if season == 'all':
                total = HarvestYield.objects.filter(harvest__status="Succeeded").filter(tree=t).aggregate(Sum('total_in_lb'))
                total_times = Harvest.objects.filter(status="Succeeded").filter(trees__in=[t]).count()
            else:
                total = HarvestYield.objects.filter(harvest__status="Succeeded").filter(tree=t).filter(harvest__start_date__year=season).aggregate(Sum('total_in_lb'))
                total_times = Harvest.objects.filter(start_date__year=season).filter(status="Succeeded").filter(trees__in=[t]).count()
            if total.get('total_in_lb__sum') is not None:
                total_tuple = (t.fruit_name, total_times, total.get('total_in_lb__sum'))
                total_list.append(total_tuple)
        return total_list

    def get_total_weight_per_neighborhood(self, season):
        nn = Neighborhood.objects.all().order_by('name')
        total_list = []
        for n in nn:
            if season == 'all':
                total = HarvestYield.objects.filter(harvest__status="Succeeded").filter(harvest__property__neighborhood=n).aggregate(Sum('total_in_lb'))
                total_times = Harvest.objects.filter(status="Succeeded").filter(property__neighborhood=n).count()
            else:
                total = HarvestYield.objects.filter(harvest__status="Succeeded").filter(harvest__property__neighborhood=n).filter(harvest__start_date__year=season).aggregate(Sum('total_in_lb'))
                total_times = Harvest.objects.filter(start_date__year=season).filter(status="Succeeded").filter(property__neighborhood=n).count()
            print total
            if total.get('total_in_lb__sum') is not None:
                total_tuple = (n, total_times, total.get('total_in_lb__sum'))
                total_list.append(total_tuple)
        return total_list

    def get_total_weight_per_beneficiary(self, season):
        beneficiaries = Organization.objects.all().order_by('civil_name')
        total_list = []
        for beneficiary in beneficiaries:
            if season == 'all':
                total = HarvestYield.objects.filter(harvest__status="Succeeded").filter(recipient=beneficiary).aggregate(Sum('total_in_lb'))
                total_times = HarvestYield.objects.filter(harvest__status="Succeeded").filter(recipient=beneficiary).count()
            else:
                total = HarvestYield.objects.filter(harvest__status="Succeeded").filter(recipient=beneficiary).filter(harvest__start_date__year=season).aggregate(Sum('total_in_lb'))
                total_times = HarvestYield.objects.filter(harvest__status="Succeeded").filter(harvest__start_date__year=season).filter(recipient=beneficiary).count()
            if total.get('total_in_lb__sum') is not None:
                total_tuple = (beneficiary, total_times, total.get('total_in_lb__sum'))
                total_list.append(total_tuple)
        return total_list

    def get_total_weight_per_picker(self, season):
        beneficiaries = Person.objects.all().order_by('first_name')
        total_list = []
        total_tuple = ()
        for beneficiary in beneficiaries:
            if season == 'all':
                total = HarvestYield.objects.filter(harvest__status="Succeeded").filter(recipient=beneficiary).aggregate(Sum('total_in_lb'))
                total_times_leader = Harvest.objects.filter(status="Succeeded").filter(pick_leader__person=beneficiary).count()
	        total_times_rfp = RequestForParticipation.objects.filter(picker=beneficiary).count()
                total_times_is_accepted = RequestForParticipation.objects.filter(picker=beneficiary).filter(is_accepted=True).count()
                total_times_recipient = HarvestYield.objects.filter(harvest__status="Succeeded").filter(recipient=beneficiary).count()
            else:
                total = HarvestYield.objects.filter(harvest__status="Succeeded").filter(recipient=beneficiary).filter(harvest__start_date__year=season).aggregate(Sum('total_in_lb'))
                # FIXME: we need a single place for picker stats. Some are
                # recipients wihout being in RequestForParticipation (maybe they're pickleaders?)
                total_times_leader = Harvest.objects.filter(status="Succeeded").filter(start_date__year=season).filter(pick_leader__person=beneficiary).count()
                total_times_rfp = RequestForParticipation.objects.filter(harvest__start_date__year=season).filter(picker=beneficiary).count()
                total_times_is_accepted = RequestForParticipation.objects.filter(harvest__start_date__year=season).filter(picker=beneficiary).filter(is_accepted=True).count()
                total_times_recipient = HarvestYield.objects.filter(harvest__status="Succeeded").filter(harvest__start_date__year=season).filter(recipient=beneficiary).count()
            if total_times_rfp > 0 or total_times_recipient > 0 or total_times_leader > 0 or total.get('total_in_lb__sum') is not None or total_times_is_accepted > 0:
                total_tuple = (beneficiary, total_times_leader, total_times_rfp, total_times_is_accepted, total_times_recipient, total.get('total_in_lb__sum'))
                total_list.append(total_tuple)
        return total_list

    def get_pickers_info(self, season):
        pickers = Person.objects.all().order_by('first_name')
        total_list = []
        for beneficiary in beneficiaries:
            if season == 'all':
                total = HarvestYield.objects.filter(harvest__status="Succeeded").filter(recipient=beneficiary).aggregate(Sum('total_in_lb'))
                total_times = HarvestYield.objects.filter(harvest__status="Succeeded").filter(recipient=beneficiary).count()
            else:
                total = HarvestYield.objects.filter(harvest__status="Succeeded").filter(recipient=beneficiary).filter(harvest__start_date__year=season).aggregate(Sum('total_in_lb'))
	        # FIXME: we need a single place for picker stats. Some are
	        # recipients wihout being in RequestForParticipation (maybe they're pickleaders?)
	        # total_times = RequestForParticipation.objects.filter(picker=beneficiary).count()
                total_times = HarvestYield.objects.filter(harvest__start_date__year=season).filter(harvest__status="Succeeded").filter(recipient=beneficiary).count()
            if total.get('total_in_lb__sum') is not None:
                total_tuple = (beneficiary, total_times, total.get('total_in_lb__sum'))
                total_list.append(total_tuple)
        return total_list
        
        

    def barchart(self):
        tt = TreeType.objects.all().order_by('fruit_name')
        xdata = []
        ydata = []
        for t in tt:
            total = HarvestYield.objects.filter(harvest__status="Succeeded").filter(tree=t).aggregate(Sum('total_in_lb'))
            if total.get('total_in_lb__sum') is not None:
                xdata.append(t.fruit_name)
                ydata.append(total.get('total_in_lb__sum'))

        extra_serie1 = {
            "tooltip": {"y_start": "", "y_end": " lb"},
        }
        chartdata = {'x': xdata, 'name1' : 'iaa', 'y1': ydata, 'extra1': extra_serie1}
        charttype = "discreteBarChart"
        chartcontainer = 'discretebarchart_container'
    
        data = {
            'charttype': charttype,
            'chartdata': chartdata,
            'chartcontainer': chartcontainer,
            'extra': {
                'x_is_date': False,
                'x_axis_format': '',
                'tag_script_js': True,
                'jquery_on_ready': False,
            }
        }
        return data
        
