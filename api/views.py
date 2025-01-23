from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import db
from datetime import datetime



class LandingAPI(APIView):
    name = 'Landing API'
    collection_name = 'coleccion'

    def get(self, request):
        ref = db.reference(f'{self.collection_name}')
        data = ref.get()
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        ref = db.reference(f'{self.collection_name}')
        current_time = datetime.now()
        custom_format = current_time.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace('am', 'a. m.').replace('pm', 'p. m.')
        request.data.update({"saved": custom_format})
        new_resource = ref.push(request.data)
        return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED)


class LandingAPIDetail(APIView):
    name = 'Landing API Detail'
    collection_name = 'coleccion'

    def get(self, request, pk):
        ref = db.reference(f'{self.collection_name}/{pk}')
        data = ref.get()
        if data:
            return Response(data, status=status.HTTP_200_OK)
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        ref = db.reference(f'{self.collection_name}/{pk}')
        if ref.get():
            ref.update(request.data)
            return Response({"message": "Updated successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        ref = db.reference(f'{self.collection_name}/{pk}')
        if ref.get():
            ref.delete()
            return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)