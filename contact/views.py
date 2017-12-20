from django.shortcuts import render_to_response, redirect
from contact.models import *
from django.template import RequestContext

from py_bing_search import PyBingWebSearch

from functools import wraps
from Contacts import settings
import random, string, os

import time
import json
import StringIO
import re
import datetime

from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt

import os

# Login Required decorator
def login_required():
    def login_decorator(function):
        @wraps(function)
        def wrapped_function(request):

            # if a user is not authorized, redirect to login page
            if 'user' not in request.session or request.session['user'] is None:
                return redirect("/")
            # otherwise, go on the request
            else:
                return function(request)

        return wrapped_function

    return login_decorator


# login view
def login(request):
    error = 'none'

    if 'username' in request.POST:

        # get username and password from request.
        username = request.POST['username']
        password = request.POST['password']

        # get a user from database based on username and password
        user = User.objects.filter(username=username, password=password)

        # check whether the user is in database or not
        if len(user) < 1:
            error = 'block'
        else:
            request.session['user'] = {
                "id": user[0].id,
                "username": user[0].username,
            }

            return redirect("/search")

    return render_to_response('login.html', {'error':error}, context_instance=RequestContext(request))


# logout view
#   initialize session variable
def logout(request):
    request.session['user'] = None
    return redirect("/")


@login_required()
def search_contact(request):

    return render_to_response('contact/input.html', locals(), context_instance=RequestContext(request))


@login_required()
def bulk_search(request):
    return render_to_response('contact/bulkInput.html', locals(), context_instance=RequestContext(request))


@login_required()
def yahoo_search(request):
    return render_to_response('contact/yahoo_finance.html', locals(), context_instance=RequestContext(request))



