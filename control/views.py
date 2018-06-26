from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader

from easy_rest.views import RestApiView

from .handlers.quadcopter_control import Drone

import time

# Create your views here.

drone = None
attitude = []
attitude_len = 100  # keeps the last attitude_len values
timeout = 0.2  # api refresh timeout


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

    @staticmethod
    def get_attitude(data):
        """
        :param data:
        :return: dictionary of the last 100 values
        """
        return {"attitude": attitude}


def run_code(request):
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
