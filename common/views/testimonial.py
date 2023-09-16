from rest_framework.response import Response
from rest_framework.views import APIView

from common.models.testimonial import Testimonial
from common.serializers.testimonial import TestimonialsSerializer


class TestimonialsListView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Testimonial.objects.all()
        serializer = TestimonialsSerializer(queryset, many=True)
        return Response(serializer.data)
