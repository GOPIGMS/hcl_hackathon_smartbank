from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Customer, Admin, Auditor, CustomerVerification

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        customer = Customer.objects.create(user=user, **validated_data)
        return customer


class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Admin
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        admin = Admin.objects.create(user=user, **validated_data)
        return admin


class AuditorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Auditor
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        auditor = Auditor.objects.create(user=user, **validated_data)
        return auditor


class CustomerVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerVerification
        fields = '__all__'
