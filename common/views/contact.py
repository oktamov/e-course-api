from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import ContactForm, ContactUs
from common.serializers import ContactFormListSerializers, ContactUsSerializer


class ContactUsListApiView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = ContactUs.objects.last()
        serializer = ContactUsSerializer(queryset)
        return Response(serializer.data)


class ContactFormView(generics.CreateAPIView):
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormListSerializers
