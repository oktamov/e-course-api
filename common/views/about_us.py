from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import AboutUs
from common.serializers import AboutUsSerializer


class AboutUsListApiViews(APIView):
    def get(self, request, *args, **kwargs):
        queryset = AboutUs.objects.last()
        serializer = AboutUsSerializer(queryset, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
