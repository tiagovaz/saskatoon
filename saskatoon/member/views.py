# coding: utf-8

from django.views import generic
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class Profile(generic.DetailView):
    model = User
    context_object_name = 'property_detail'
    template_name = 'member/profile.html'

    def dispatch(self, *args, **kwargs):
        get_object_or_404(
            User,
            id=self.kwargs['pk']
        )

        return super(Profile, self).dispatch(*args, **kwargs)
