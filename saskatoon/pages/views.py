from django.views import generic
from harvest.models import Harvest, Property
from member.models import AuthUser
from django.http import JsonResponse
from django.core.urlresolvers import reverse


class Calendar(generic.TemplateView):
    template_name = 'pages/calendar.html'

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


class Index(generic.TemplateView):
    template_name = 'pages/dashboard.html'

    def dispatch(self, *args, **kwargs):
        return super(Index, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated():
            email = self.request.user.email
            user = AuthUser.objects.get(email=email)
            context['user'] = user
            context['number_of_harvests'] = Harvest.objects.all().count()
            context['number_of_properties'] = Property.objects.all().count()
            context['number_of_users'] = AuthUser.objects.all().count()

        return context


class Login(generic.TemplateView):
    template_name = 'registration/login.html'
