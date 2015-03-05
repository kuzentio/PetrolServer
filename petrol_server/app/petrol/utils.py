from django.shortcuts import render_to_response


def render_decorator(template):
    def decorator(func):
        def inner(*args, **kwargs):
            context = func(*args, **kwargs)
            return render_to_response(template, context)
        return inner
    return decorator



