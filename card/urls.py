from django.urls import path

from card.views import CardListCreateView, CardDetailView

urlpatterns = [
    path('', CardListCreateView.as_view(), name='list-create'),
    path('<int:pk>/', CardDetailView.as_view(), name='detail'),
]
