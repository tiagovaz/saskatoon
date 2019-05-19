import datetime

from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.urls import reverse
from django.views import generic
from harvest.models import Harvest, Property


########## Original template views #############

def index(request):
    context = {}
    template = loader.get_template('app/index.html')
    return HttpResponse(template.render(context, request))


def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))

############ 'pages' views ####################

class Calendar(generic.TemplateView):
    template_name = 'app/calendar.html'

    def dispatch(self, request, *args, **kwargs):
        return super(Calendar, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Calendar, self).get_context_data(**kwargs)

        context['view'] = "calendar"

        return context

class JsonCalendar(generic.View):
    def get(self, request, *args, **kwargs):
        start_date = request.GET.get('start')
        end_date = request.GET.get('end')
        ed = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        sd = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        harvests = Harvest.objects.filter(end_date__lte=ed, start_date__gte=sd)
        events = []
        for harvest in harvests:
            if (harvest.start_date and
                    harvest.end_date and
                    self.request.user.is_staff) \
                    or harvest.is_publishable():
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
                else:
                    color = "#000000"
                event = dict()
                event["title"] = harvest.property.neighborhood.name
                event["allday"] = "false"
                event["description"] = harvest.about
                # FIXME: see
                # http://fullcalendar.io/docs/event_rendering/eventRender/
                if harvest.start_date:
                    event["start"] = harvest.start_date - \
                                     datetime.timedelta(hours=4)
                # FIXME: ugly hack, needs proper interaction with calendar
                # http://fullcalendar.io/docs/timezone/timezone/
                if harvest.end_date:
                    event["end"] = harvest.end_date - \
                                   datetime.timedelta(hours=4)
                event["url"] = reverse(
                    'harvest:participation_create',
                    kwargs={'pk': harvest.id}
                )
                event["color"] = color
                event["textColor"] = text_color
                events.append(event)
                del event

        return JsonResponse(events, safe=False)



