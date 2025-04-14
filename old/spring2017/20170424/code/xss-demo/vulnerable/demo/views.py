from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.views.decorators.clickjacking import xframe_options_exempt
import random

# Create your views here.
SECRET = int(random.uniform(0, 100000))

@xframe_options_exempt
def index(request):
    if not request.session.session_key:
        request.session.create()
        request.session['testkey'] = 'testvalue'
        request.session['danger'] = 0
    request.session.save()
    login = request.GET.get('login', '')
    if login:
        request.session['login'] = login
    value = request.GET.get('value', '')
    response = HttpResponse(
            "The value submitted was: " + value + "<br>" +
            "<form method=get>submit new value: <input name=value><input type=submit value='submit'><br><br>" +
            "<br>Your session ID is " + str(request.session.session_key) +
            "<br>That session ID is listed as logged in as: " + request.session.get('login', '(not logged in)') +
            "<br>And " + str(request.session.get('danger', 0)) + " dangerous actions performed<br><br>" +
            "<br>demo options:" +
            "<ul>" +
            "<li><a href='/demo/secret/'>a page with a secret</a>" +
            "<hr>" + 
            "<li><a href='/demo/danger/'>dangerous action page</a></li>" +
            "<li><a href='/demo/danger-nocsrf/'>dangerous action page (w/ CSRF protection)</a>" +
            "<hr>" +
            "<li><a href='/demo/readable/'>a remote readable page</a>" +
            "<li><small><a href='/demo/reset-danger/'>reset action count</a></small>" +
            "</form></li></ul>"
            )
    return response

@xframe_options_exempt
@csrf_exempt
def danger(request):
    if request.method == 'POST':
        request.session['danger'] = request.session.get('danger', 0) + 1
        return HttpResponse("Performed dangerous action!<br>" +
                str(request.session.get('danger', 0)) + " dangerous actions performed so far."
                )
    else:
        return HttpResponse(
                str(request.session.get('danger', 0)) + " dangerous actions performed" +
                "<form method='POST'><input type=submit value='Do dangerous thing!'></form>")

@xframe_options_exempt
@ensure_csrf_cookie
def danger_nocsrf(request):
    if request.method == 'POST':
        request.session['danger'] = request.session.get('danger', 0) + 1
        return HttpResponse("Performed dangerous action<br>" +
                str(request.session.get('danger', 0)) + " dangerous actions performed so far."
                )
    else:
        return HttpResponse(
                str(request.session.get('danger', 0)) + " dangerous actions performed" +
                "<form method='POST'><input type=submit value='Do dangerous thing!'><br>" +
                "CSRF token (normally hidden): <input name=csrfmiddlewaretoken value='" +
                get_token(request) + "'><br>" +
                "</form>")



def reset_danger(request):
    request.session['danger'] = 0
    return HttpResponse("Reset Danger")


@csrf_exempt
def danger_noframe(request):
    if request.method == 'POST':
        request.session['danger'] = request.session.get('danger', 0) + 1
        return HttpResponse("Performed dangerous action!<br>" +
                str(request.session.get('danger', 0)) + " dangerous actions performed so far."
                )
    else:
        return HttpResponse(
                str(request.session.get('danger', 0)) + " dangerous actions performed" +
                "<form method='POST'><input type=submit value='Do dangerous thing!'></form>")

@xframe_options_exempt
def secret(request):
    return HttpResponse(
            "The secret value is <span id='secret'>" + str(SECRET) + "</span>"
    )

@xframe_options_exempt
def secret_noframe(request):
    return HttpResponse(
            "The secret value is <span id='secret'>" + str(SECRET) + "</span>"
    )

@xframe_options_exempt
def readable(request):
    response = HttpResponse(
        "Here the secret value <span id='secret'>" + str(SECRET) + "</span> is readable remotely " +
        "(but not via iframes)<br>" +
        "The Origin header was <b>" + str(request.META.get('HTTP_ORIGIN', '<i>unset</i>')) + "</b>."
    )
    response['Access-Control-Allow-Origin'] = '*';
    return response
