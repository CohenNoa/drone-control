from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader

from .handlers.quadcopter_control import Drone

# Create your views here.

drone = None


def home_page(request):
    template = loader.get_template('control/home_page.html')
    context = {}
    return HttpResponse(template.render(context, request))


def index(request):
    template = loader.get_template('control/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


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
            drone.run_command(command)
    except NameError as err:
        error = 'Drone not initialized: ' + str(err)
    response = {
        'success': True,
        'error': error
    }
    return JsonResponse(response)
