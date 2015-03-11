from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response


def render_decorator(template):
    def decorator(func):
        def inner(*args, **kwargs):
            context = func(*args, **kwargs)
            return render_to_response(template, context)
        return inner
    return decorator


def staff_required(redirect_url):
    def decorator(func):
        def wrapper(request):
            if request.user.is_staff:
                return HttpResponseRedirect(redirect_url)
            return func(request)
        return wrapper
    return decorator



