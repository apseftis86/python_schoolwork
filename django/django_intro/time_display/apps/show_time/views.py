from django.shortcuts import render
# from time import gmtime, strftime
from datetime import datetime

def index(request):

    context = {
        "time": datetime.now()
    }
    return render(request, 'show_time/index.html', context)