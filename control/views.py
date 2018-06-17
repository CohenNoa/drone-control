from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader

from easy_rest.views import RestApiView

from .handlers.quadcopter_control import Drone

# Create your views here.

drone = None
attitude = []
attitude_len = 400


def home_page(request):
    template = loader.get_template('control/home_page.html')
    context = {}
    return HttpResponse(template.render(context, request))


def index(request):
    template = loader.get_template('control/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def live_data(request):
    template = loader.get_template('control/live_data.html')
    context = {}
    return HttpResponse(template.render(context, request))


class AttitudeGraphApiView(RestApiView):
    function_field_name = "action"
    api_allowed_methods = ["get_attitude"]

    def get_attitude(self, data):
        return {"attitude": attitude}


def run_code(request):
    global drone
    command = request.GET.get('command', None)
    if command == 'start' and not drone:
        drone = Drone()
        drone.arm()
    if command == 'stop' and drone:
        drone.disarm()
        drone = None
    error = None
    try:
        if drone and command not in ["start", "stop"]:
            build_data(command.split("_"))
            print(attitude)
            drone.run_command(command)
    except NameError as err:
        error = 'Drone not initialized: ' + str(err)
    response = {
        'success': True,
        'error': error
    }
    return JsonResponse(response)


def build_data(new_data):
    global attitude
    if len(attitude) < attitude_len:
        attitude.append(new_data)
    else:
        temp_data = attitude[-attitude_len:]
        temp_data.append(new_data)
        attitude = temp_data
