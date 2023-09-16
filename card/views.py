from rest_framework import generics, permissions

from card.models import Card
from card.serializers import CardSerializer
from permissions import IsCardUser


class CardListCreateView(generics.ListCreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)


class CardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsCardUser]
    lookup_field = 'pk'
