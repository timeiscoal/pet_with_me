from rest_framework.authentication import BaseAuthentication 
from rest_framework.exceptions import AuthenticationFailed
from users.models import User
import jwt
from django.conf import settings

# 장고에게 USER를 찾는 방법을 알려줌 . header을 통해서 ;;
# sessionAuthentication이라는 class가 쿠키랑 세션을 보고 유저를 찾는다. 이 클래스는 지정한 authentication을 찾는다.

# 기본 설정으로 django rest framework는 백엔드에서 쿠키와 세션을 보고 ,  ㅕuser가 누구인지 확인함. 그게 request.user
# 커스텀하는 방법은 새로운 클래스를 만들고 baseAuthenication을 상속하면됨.
# 이 상속받은 class스 안에 authenitcation이 api호출시 우선적으로 동작함.
# request는 헤더나 쿠키, url ip주소 같은 정보들을 가지고 있다.

# 토큰을 backend에서 보관하고 관리하면 너무 많은 용량을 차지할 수 있다.


class CustomAuthentication(BaseAuthentication):

    def authenticate(self, request):
        
        email = request.headers.get('test')
        if not email:
            return None
        
        try:
            # user가 없다면? 에러 
            user =User.objects.get(email=email)
            # user, None 이게 룰임;
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed(f"NO eamil {email}")
        


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        
        # 헤더
        token = request.headers.get("token")
         # 토큰 안보내면 none
        if not token:
            return None
        # 복호화
        decoded= jwt.decode(token, settings.SECRET_KEY, algorithms="HS256",)

        pk = decoded.get("pk")
        # 토큰을 디코딩했는데 유효하지 않은 토큰이면 에러

        if not pk:
            return AuthenticationFailed("유효하지 않은 토큰입니다.")
        try:
            user = User.objects.get(pk=pk)
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed("사용자를 찾지 못했습니다.")

