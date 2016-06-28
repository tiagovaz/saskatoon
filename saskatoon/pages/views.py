from django.views import generic
from harvest.models import Harvest, Property
from member.models import AuthUser
from django.http import JsonResponse
from django.core.urlresolvers import reverse
import datetime

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
        harvests = Harvest.objects.all()
        events = []
        for harvest in harvests:
            if harvest.is_publishable():
                text_color = "#ffffff"
                if harvest.status == "Date-scheduled":
                    color = "#f0ad4e"
                elif harvest.status == "Ready":
                    color = "#5cb85c"
                elif harvest.status == "Succeeded":
                    color = "#337ab7"
                elif harvest.status == "Cancelled":
                    color = "#f9f9f9"
                    text_color = "#000000"
                event = {}
                event["title"] = harvest.property.neighborhood.name
                event["allday"] = "false"
                event["description"] = harvest.about #FIXME: see http://fullcalendar.io/docs/event_rendering/eventRender/
                if harvest.start_date:
                    event["start"] = harvest.start_date - datetime.timedelta(hours=4) #FIXME: ugly hack, needs proper interaction with calendar (http://fullcalendar.io/docs/timezone/timezone/)
                if harvest.end_date:
                    event["end"] = harvest.end_date - datetime.timedelta(hours=4)
                event["url"] = reverse(
                    'harvest:harvest_detail',
                    kwargs={'pk': harvest.id}
                )
                event["color"] = color
                event["textColor"] = text_color
                events.append(event)
                del event

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
