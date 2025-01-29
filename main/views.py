from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from datetime import datetime
from collections import Counter
import requests
import json

@login_required 
@permission_required('main.index_viewer', raise_exception=True)
def index(request):
    # Construir el endpoint del REST API
    current_url = request.build_absolute_uri()
    url = current_url + '/api/v1/landing'

    # Petición al REST API
    response_http = requests.get(url)
    response_dict = json.loads(response_http.content)

    def clean_datetime(date_str):
        """Corrige el formato de fecha y la convierte a datetime."""
        try:
            date_str = date_str.replace("\xa0", " ")  # Eliminar espacios no rompibles
            date_str = date_str.strip().replace("a. m.", "AM").replace("p. m.", "PM")  # Arreglar formato
            parsed_date = datetime.strptime(date_str, "%d/%m/%Y, %I:%M:%S %p")
            return parsed_date
        except Exception as e:
            print(f"Error al convertir fecha: {date_str} -> {e}")
            return None  # Devolver None si la fecha es inválida

    try:
        # Convertir a una lista de tuplas (clave, valores) con fechas válidas
        valid_items = [(key, value, clean_datetime(value["saved"])) for key, value in response_dict.items()]
        
        # Filtrar los que no tienen fecha válida
        valid_items = [(key, value, date) for key, value, date in valid_items if date is not None]

        # Agrupar por día de la semana (0=lunes, 6=domingo)
        day_counts = Counter([date.weekday() for _, _, date in valid_items])

        # Convertir los números de día a nombres de días
        day_names = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        day_with_most_responses = day_names[max(day_counts, key=day_counts.get)] if day_counts else "No hay datos"

        # Mostrar el día con más respuestas
        print(f"Día con más respuestas: {day_with_most_responses}")

        # Si no hay datos válidos, asignamos listas vacías
        if not valid_items:
            sorted_items = []
        else:
            sorted_items = sorted(valid_items, key=lambda x: x[2])  # Ordenar por la fecha

        # Depuración: Mostrar orden final de las fechas
        for item in sorted_items:
            print(f"Email: {item[1]['email']} | Fecha: {item[2]}")

        # Respuestas totales
        total_responses = len(response_dict.keys())

        # Objeto con los datos a renderizar
        data = {
            'title': 'Landing - Dashboard',
            'total_responses': total_responses,
            'responses': response_dict.values(),
            'first_email': sorted_items[0][1]["email"].split('@')[0] if sorted_items else None,
            'last_email': sorted_items[-1][1]["email"].split('@')[0] if sorted_items else None,
            'day_with_most_responses': day_with_most_responses
        }

    except Exception as e:
        print("Error al procesar las fechas:", e)
        data = {'title': 'Landing - Dashboard', 'total_responses': 0, 'responses': [], 'day_with_most_responses': "Error"}

    # Renderización en la plantilla
    return render(request, 'main/index.html', data)