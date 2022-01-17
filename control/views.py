from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, reverse

from easy_rest.views import RestApiView

from .handlers.quadcopter_control import Drone

import time

# Create your views here.

drone = None
attitude = []
attitude_len = 100  # keeps the last attitude_len values
timeout = 0.2  # api refresh timeout
index_online_users = []  # saves the current user's ip that connect index page
INDEX_ONLINE = 1  # number of users that can use the index page at the same time


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse("homepage"))
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def home_page(request):
    template = loader.get_template('control/home_page.html')
    context = {}
    return HttpResponse(template.render(context, request))


def index(request):
    # if request.user.is_authenticated:
    template = loader.get_template('control/index.html')
    context = {}
    # else:
    #     template = loader.get_template('control/error.html')
    #     context = {'header': '403 Access Denied',
    #                'data': 'You are not authorized to access this page'}
    return HttpResponse(template.render(context, request))


def live_data(request):
    # if request.user.is_authenticated:
    template = loader.get_template('control/live_data.html')
    context = {}
    # else:
    #     template = loader.get_template('control/error.html')
    #     context = {'header': '403 Access Denied',
    #                'data': 'You are not authorized to access this page'}
    return HttpResponse(template.render(context, request))


class AttitudeGraphApiView(RestApiView):
    function_field_name = "action"
    api_allowed_methods = ["get_attitude"]

    @staticmethod
    def get_attitude(data):
        """
        :param data:
        :return: dictionary of the last 100 values
        """
        return {"attitude": attitude}


def run_code(request):
    """
    handles ajax command from index page
    :param request:
    :return:
    """
    global drone
    global attitude
    command = request.GET.get('command', None)
    if command == 'start' and not drone:
        drone = Drone()
        drone.arm()
        attitude = []

        # updates graph on arm
        build_data(['attitude', 'pitch', '0'])
        time.sleep(timeout)
        build_data(['attitude', 'yaw', '100'])
        time.sleep(timeout)
        build_data(['attitude', 'roll', '0'])
        time.sleep(timeout)
        build_data(['attitude', 'throttle', '0'])
        time.sleep(timeout)

    if command == 'stop' and drone:
        drone.disarm()
        drone = None

        # updates graph on disarm
        build_data(['attitude', 'pitch', '0'])
        time.sleep(timeout)
        build_data(['attitude', 'yaw', '0'])
        time.sleep(timeout)
        build_data(['attitude', 'roll', '100'])
        time.sleep(timeout)
        build_data(['attitude', 'throttle', '0'])
        time.sleep(timeout)

        attitude = []

    if command == "connect":
        # user login index page
        ip_addr = request.META['REMOTE_ADDR']  # IPv4 address
        if ip_addr not in index_online_users:
            index_online_users.append(ip_addr)
        if len(index_online_users) > INDEX_ONLINE:
            return JsonResponse({'success': False, 'error': 'error'})  # too many users use the template
        return JsonResponse({'success': True})  # user can get the template

    if command == "disconnect":
        # user logout index page
        ip_addr = request.META['REMOTE_ADDR']  # IPv4 address
        index_online_users.remove(ip_addr)

    error = None
    try:
        if drone and command not in ["start", "stop"]:
            # action is something else then button click
            build_data(command.split("_"))
            drone.run_command(command)
    except NameError as err:
        error = 'Drone not initialized: ' + str(err)
    response = {
        'success': True,
        'error': error
    }
    return JsonResponse(response)


def build_data(new_data):
    """
    adds new piece of data to attitude list
    :param new_data:
    :return:
    """
    global attitude
    if len(attitude) < attitude_len:
        attitude.append(new_data)
    else:
        temp_data = attitude[-attitude_len:]
        temp_data.append(new_data)
        attitude = temp_data
