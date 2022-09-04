from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator
from .utils import verifyNumber

class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
        )
    username = serializers.CharField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
        )
    otp = serializers.CharField(required=True)

    class Meta:
        model = User
        exclude = ['is_admin', 'is_active', 'is_superuser', 'password', 'last_login']
        read_only_fields = ['id', 'volunteerScore', 'sessions']
        extra_kwargs = {
            'phone': {'write_only': True},
            'countryCode': {'write_only': True},
        }

    def validate(self, attrs):
        countryCode = attrs["countryCode"]
        phone = attrs['phone']
        if not verifyNumber(f"{countryCode}{phone}", attrs['otp']):
            raise serializers.ValidationError({"phone_number": "OTP verification failed"})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            phone=validated_data['phone'],
            countryCode=validated_data['countryCode'],
        )

        user.save()
        return user

class sessionsSerializer(serializers.ModelSerializer):
    topic = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Session.objects.all())]
    )

    class Meta:
        model = Session
        fields = "__all__"
        read_only_fields = ['id']

class messageDetail(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['id', 'text', 'sender', 'created_at']
        read_only_fields = ['id']

    def to_representation(self, instance):
        m = super(messageDetail, self).to_representation(instance)
        m['sender'] = instance.sender.username
        return m

class messageSerializer(serializers.ModelSerializer):
    messages = messageDetail(many=True)

    class Meta:
        model = Session
        fields = "__all__"
        read_only_fields = ['id']
