import xlrd
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response


@login_required(login_url='accounts/login/')
def main(request):
    if request.user.is_staff:
        return render_to_response('upload_file.html')
    return render_to_response('index.html')


@login_required(login_url='account/login/')
def upload_file(request):
    workbook = xlrd.open_workbook(request.GET['transactions'])
    import ipdb; ipdb.set_trace()


    #TODO: Use django-import-export api - https://django-import-export.readthedocs.org/en/latest/getting_started.html

    return HttpResponse('<p>Hello World</p>')







