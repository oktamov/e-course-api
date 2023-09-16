from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import Banner
from common.serializers import BannerSerializer


class BannerApiView(APIView):
    def get(self, request, *args, **kwargs):
        banners = Banner.objects.order_by("position").first()
        serializer = BannerSerializer(banners, context={"request": request})
        return Response(serializer.data)
