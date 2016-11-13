# Model serializers
from rest_framework import serializers
from trader.models import UserProfile, Category, SaleItem

class SaleItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = SaleItem
        fields = ('id', 'sold_status', 'created_on', 'primary_image',
                  'secondary_image', 'optional_image', 'description',
                  'price')

class CategorySerializer(serializers.ModelSerializer):
    sale_items = SaleItemSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent_category', 'depth', 'all_items')

class RootCategorySerializer(serializers.ModelSerializer):
    sale_items = SaleItemSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'depth')

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    sale_items = SaleItemSerializer(many=True)

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'sale_items')
