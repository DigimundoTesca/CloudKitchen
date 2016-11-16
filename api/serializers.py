from rest_framework import serializers
from supplies.models import CustomerOrder, CustomerOrderDetail, Cartridge, PackageCartridge, PackageCartridgeRecipe, \
    User, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',)


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=UserProfile.objects.all(), source='user')
    
    class Meta:
        model = UserProfile
        fields = ('user', 'user_id', 'phone_number',)


class CartridgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cartridge
        fields = ('id', 'name', 'price', 'category', 'image')


class PackageCartridgeRecipeSerializer(serializers.ModelSerializer):
    cartridge = CartridgeSerializer(read_only=True)
    
    class Meta:
        model = PackageCartridgeRecipe
        fields = ('id', 'cartridge', 'quantity',)


class PackageCartridgeSerializer(serializers.ModelSerializer):
    package_cartridge_recipe = PackageCartridgeRecipeSerializer(many=True, read_only=True,
                                                                source='packagecartridgerecipe_set')
    
    class Meta:
        model = PackageCartridge
        fields = ('id', 'name', 'price', 'package_cartridge_recipe', 'image')


class CustomerOrderDetailSerializer(serializers.ModelSerializer):
    cartridge = CartridgeSerializer(read_only=True, )
    package_cartridge = PackageCartridgeSerializer(read_only=True, )
    
    class Meta:
        model = CustomerOrderDetail
        fields = ('id', 'cartridge', 'package_cartridge', 'quantity',)


class CustomerOrderSerializer(serializers.ModelSerializer):
    customer_order_details = CustomerOrderDetailSerializer(many=True, read_only=True, source='customerorderdetail_set')
    customer_user = UserProfileSerializer(read_only=True,)
    customer_user_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=UserProfile.objects.all(), source='customer_user')

    class Meta:
        model = CustomerOrder
        fields = (
            'id', 'created_at', 'delivery_date', 'customer_user', 'customer_user_id', 'customer_order_details', 'status', 'price',
            'latitude', 'longitude',)
