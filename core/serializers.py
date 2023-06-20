from rest_framework import serializers
from .models import HomeSlider, HomeBlock, Products, Categories, Collections

class HomeSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeSlider
        fields = ('slideName','is_active','isMobile','slide')


class HomeBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeBlock
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = "__all__"

class CollectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collections
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    collections = CollectionsSerializer()
    class Meta:
        model = Products
        fields = "__all__"