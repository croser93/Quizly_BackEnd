from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuth(JWTAuthentication):

    def authenticate(self, request):
        access = request.COOKIES.get('access_token')
        
        if access is None:
            return None
        
        validated = self.get_validated_token(access)
        user = self.get_user(validated_token = validated)
        return (user, validated)
        
