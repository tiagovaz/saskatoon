from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from user_profile.models import AuthUser
from main.models import Harvest, EquipmentType
from main.forms import NewEquipment, NewHarvest
from django_bootstrap_calendar.models import CalendarEvent
from django.http import HttpResponse

from fixtureless import Factory
import itertools

# Inserting random data
class DataTest(View):
    def get(self, request):
        factory = Factory()
        count = 1
        initial = {
            'description': 'test description',
        }
        initial_list = list()
        for _ in itertools.repeat(None, count):
            initial_list.append(initial)
        h = factory.create(Harvest, initial_list)
        self.insert_to_calendar()
        return HttpResponseRedirect('/harvests/')
    
    def insert_to_calendar(self):
        factory = Factory()
        count = 10
        initial = {
            'title': 'test title for calendar',
        }
        initial_list = list()
        for _ in itertools.repeat(None, count):
            initial_list.append(initial)
        c = factory.create(CalendarEvent, initial_list)
        
    def insert_to_et(self):
        factory = Factory()
        c = factory.create(EquipmentType, 10)


class EquipmentForm(View):
    def get(self, request):
        equipment_form = NewEquipment()
        return render(request, 'form_new_equipment.html', {'form': equipment_form})

    def post(self, request):
        params = dict()
        equipment = NewEquipment(request.POST)
        new_equipment = equipment.save()
        if equipment.is_valid():
            return HttpResponseRedirect('/new_equipment/')

class HarvestForm(View):
    def get(self, request):
        harvest_form = NewHarvest()
        return render(request, 'form_new_harvest.html', {'form': harvest_form})

    def post(self, request):
        params = dict()
        harvest = NewHarvest(request.POST)
        new_harvest = harvest.save()
        if harvest.is_valid():
            return HttpResponseRedirect('/new_harvest/')

class Calendar(View):
    def get(self, request):
        return render(request, 'calendar.html')


class Harvests(View):
    def get(self, request):
        params = dict()
        all_harvests = Harvest.objects.all()
        params["harvests"] = all_harvests
        return render(request, 'harvests.html', params)

class Profile(View):
    def get(self, request, username):
        params = dict()
        user = AuthUser.objects.get(username=username)
        params["user"] = user
        return render(request, 'profile.html', params)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class Index(View):
    def get(self, request):
        params = dict()
        email = None
        if request.user.is_authenticated():
            email = request.user.email
            user = AuthUser.objects.get(email=email)
            params["user"] = user
            return render(request, 'dashboard.html', params)
        else:
            return render(request, 'login.html', params)

    # Index also handles authentication from login form
    def post(self, request):
        params = dict()
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render(request, 'login.html', params)
                # TODO: Return a 'disabled account' error message
        else:
            return render(request, 'login.html', params)
            # TODO: Return an 'invalid login' error message.
