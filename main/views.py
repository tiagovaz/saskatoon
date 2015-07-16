from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from user_profile.models import AuthUser
from main.models import Harvest, Property
from main.forms import NewEquipment, NewHarvest

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

class Index(View):
    def get(self, request):
        params = dict()
        username = None
        if request.user.is_authenticated():
            username = request.user.username
            user = AuthUser.objects.get(username=username)
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
