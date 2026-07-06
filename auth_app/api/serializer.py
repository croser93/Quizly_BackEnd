from rest_framework import serializers
from django.contrib.auth.models import User

class RegisstrationSerializer(serializers.ModelSerializer):

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
        confirmed_pw = self.validated_data['confirmed_password']
        email = self.validated_data['email']

        all_emails = User.objects.values_list('email', flat=True)

        if pw != confirmed_pw:
            raise serializers.ValidationError({'error': 'password dont match' })
        
        if email in all_emails:
            raise serializers.ValidationError({'error' : 'email exist'})
        
        account = User (
            username = username,
            email = email
        )

        account.set_password(pw)
        account.save
        return account