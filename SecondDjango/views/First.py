from django.http import HttpResponse

# return static content
def index(request):
    return HttpResponse('Pycharm')

