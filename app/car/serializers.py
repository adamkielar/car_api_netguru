from django.db.models import Avg, Count
from rest_framework import serializers

from core.models import Car, Rating


class CarListSerializer(serializers.ModelSerializer):
    """Serializer for list of cars"""
    ratings = serializers.HiddenField(
        default=serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    )
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = (
            'id',
            'car_make',
            'car_model',
            'ratings',
            'average_rating'
        )
        read_only_fields = ('id',)

    def get_average_rating(self, obj):
        average = obj.ratings.aggregate(Avg('rating')).get('rating__avg')

        if average is None:
            return 0
        return round(average * 2) / 2


class CarAddSerializer(serializers.ModelSerializer):
    """Serializer for car creation"""

    class Meta:
        model = Car
        fields = (
            'id',
            'car_make',
            'car_model',
        )
        read_only_fields = ('id',)


class CarPopularSerializer(serializers.ModelSerializer):
    """Serializer for top 10 cars"""

    class Meta:
        model = Car
        fields = (
            'id',
            'car_make',
            'car_model',
#            'rating_count',
        )
        read_only_fields = ('id', )


class CarRatingSerializer(serializers.ModelSerializer):
    """Serializer to add ratings"""

    class Meta:
        model = Rating
        fields = (
            'id',
            'car',
            'rating',
        )
        read_only_fields = ('id',)

    def validate_rating(self, value):
        if value in range(1, 6):
            return value
        raise serializers.ValidationError(
            "Rating must be an integer between 1 and 5"
        )
