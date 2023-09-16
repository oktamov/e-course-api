from rest_framework import serializers

from common.models import Board, BoardLogoTitle


class BoardLogoTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardLogoTitle
        fields = ('logo', 'title', 'url')


class BoardTextSerializer(serializers.ModelSerializer):
    boards = BoardLogoTextSerializer(many=True)

    class Meta:
        model = Board
        fields = ('title', 'boards')
