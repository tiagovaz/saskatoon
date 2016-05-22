from django.views import generic
from harvest.models import *
from django.contrib.auth.models import User


class Index(generic.TemplateView):
    template_name = 'pages/dashboard.html'

    def dispatch(self, *args, **kwargs):
        return super(Index, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated():
            email = self.request.user.email
            user = User.objects.get(email=email)
            context['user'] = user
            context['number_of_harvests'] = Harvest.objects.all().count()
            context['number_of_properties'] = Property.objects.all().count()
            context['number_of_users'] = User.objects.all().count()

        return context


class Login(generic.TemplateView):
    template_name = 'registration/login.html'
