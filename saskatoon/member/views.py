# coding: utf-8
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from models import Person, AuthUser
from member.filters import PersonFilter


class Profile(generic.DetailView):
    model = User
    context_object_name = 'profile'
    template_name = 'member/profile.html'

    def dispatch(self, *args, **kwargs):
        get_object_or_404(
            User,
            id=self.kwargs['pk']
        )
        return super(Profile, self).dispatch(*args, **kwargs)


        active_properties = Property.objects.filter(authorized=True)
        all_properties = PropertyFilter(
            request,
            queryset
        )


        return context


class PeopleList(generic.ListView):
    template_name = 'member/list.html'
    context_object_name = 'people'
    model = AuthUser

    def get_queryset(self):
        request = self.request.GET
        queryset = AuthUser.objects.all()
        return PersonFilter(
            request,
            queryset
        )

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PeopleList, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PeopleList, self).get_context_data(**kwargs)
        request = self.request.GET.copy()
        queryset = AuthUser.objects.all().order_by('-id')
        people = PersonFilter(
            request,
            queryset
        )
        context['view'] = "people"
        context['people'] = people
        context['form'] = people.form

        return context
