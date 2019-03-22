from django.shortcuts import render
import datetime
import time
import requests
from django.http import Http404

def main(request):
    time = datetime.datetime.now().strftime("%H:%M:%S")
    try:    
        resp = requests.get(
        "http://api.openweathermap.org/data/2.5/weather",
        params={
                "q": "Minsk",
                "APPID": "454caf0086d06d8471d25097146af0db",
                'units': 'metric'
        })
        resp_five =requests.get(
        "http://api.openweathermap.org/data/2.5/forecast",
        params={
                "q": "Minsk",
                "APPID": "454caf0086d06d8471d25097146af0db",
                'units': 'metric'
        })
    except:
            raise Http404
    
    data_five = resp_five.json()
    data = resp.json()
    weather = data
    weather = str(data['main']['temp']) + '°C, ' + data['weather'][0]['main'] 
    
    data_graph = []
    data_time = []
    data_wind = []
    for x in range(1,8):
        part_data = data_five['list'][x]['main']['temp']
        part_time = data_five['list'][x]['dt_txt']
        part_wind = data_five['list'][x]['wind']['speed']
        data_graph.append(part_data)
        data_time.append(int(part_time[11:13]))
        data_wind.append(part_wind)
    

    context= {'var':10,
             'user': request.user, 
             'date': datetime.date.today(),
             'time': time,
             'weather': weather,
             'data_graph' : data_graph,
             'icon': data['weather'][0]['icon'],
             'pressure': data['main']['pressure'],
             'humidity': data['main']['humidity'],
             'wind': data['wind']['speed'],
             'data_graph': data_graph,
             'data_time': data_time ,
             'data_graph_wind': data_wind,
            }
    return render(request, 'dashboard/index.html', context)
    
