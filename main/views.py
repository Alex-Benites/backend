from django.shortcuts import render
# Importe el decorador login_required
from django.contrib.auth.decorators import login_required
# Importe el decorador login_required
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
from django.http import HttpResponse



import requests
import json

@login_required 
@permission_required('main.index_viewer', raise_exception=True)
def index(request):
        
    # Arme el endpoint del REST API
    current_url = request.build_absolute_uri()
    url = current_url + '/api/v1/landing'

    # Petición al REST API
    response_http = requests.get(url)
    response_dict = json.loads(response_http.content)

    print("Endpoint ", url)
    print("Response ", response_dict)

    # Respuestas totales
    total_responses = len(response_dict.keys())

    responses = response_dict.values()

    # Objeto con los datos a renderizar
    data = {
        'title': 'Landing - Dashboard',
        'total_responses': total_responses,
        'responses': responses,
    }

    # Valores de la respuesta
    

    # Renderización en la plantilla
    return render(request, 'main/index.html', data)
