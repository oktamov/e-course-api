from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import Board
from common.serializers import BoardTextSerializer


class BoardTextView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Board.objects.filter(is_active=True)
        serializer = BoardTextSerializer(queryset, many=True)
        return Response(serializer.data)
