from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
class RegisstrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.

    confirmed_password = write-only field used to confirm the password matches
    """

    confirmed_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["username", "password", "confirmed_password", "email"]
        extra_kwargs = {
            'password' : {'write_only' : True},
            'email' : {'required' : True}
        }

    def save(self, **kwargs):
        username = self.validated_data['username']
        pw = self.validated_data['password']
        confirmed_password = self.validated_data['confirmed_password']
        email = self.validated_data['email']

        all_emails = User.objects.values_list('email', flat=True)

        if pw != confirmed_password:
            raise serializers.ValidationError({'error': 'password dont match' })
        
        if email in all_emails:
            raise serializers.ValidationError({'error' : 'email exist'})
        
        account = User (
            username = username,
            email = email
        )

        account.set_password(pw)
        account.save()
        return account
    
class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.

    username = write-only field containing the login username
    password = write-only field containing the login password
    """

    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']    
    
    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])

        if(user):
            return {'user': user}
        else:
            raise serializers.ValidationError({'error': 'wrong credentials'})