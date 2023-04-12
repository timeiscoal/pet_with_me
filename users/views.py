from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from django.contrib.auth import login, logout ,authenticate

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.conf import settings
from django.db import transaction

from users.models import User
from calendars.models import TodoCategory
import jwt


from calendars.serializers import TodoCategorySerializer ,ChallengeCreateSerializer
from users.serializers import ProfileSerializer ,UserSerializer ,UserCreateSerializer ,ProfilePutSerializer,RegisterSerializer ,SimpleJWTLoginSerialzier

# Create your views here.


class Me(APIView):

    # permission_classes = [IsAuthenticated]

    def get(self ,request):
        user = request.user
        return Response(ProfileSerializer(user).data)

    def delete(self,request, ):

        user = request.user
        if user:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"에러발생"}, status=status.HTTP_400_BAD_REQUEST)
        # return Response({"message":"권한이 없습니다."},status=status.HTTP_401_UNAUTHORIZED)

# 사용자 개인정보 / 조회 / 수정 / 삭제 (탈퇴)

class MyProfileView(APIView):


    def get(self, request, user_id):
        users = User.object.get(id=user_id) 

        if request.user == users:
            serializer = ProfileSerializer(users)
            return Response(serializer.data , status=status.HTTP_200_OK )
        else:
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    
    def put(self, request, user_id):
        users = User.objects.get(id=user_id)
        print(request.data)
        serializer = ProfilePutSerializer(users , data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request, user_id):
        users = User.objects.get(id=user_id)
        if request.user == users:
            users.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"권한이 없습니다."},status=status.HTTP_401_UNAUTHORIZED)


# 사용자 회원 가입
# 사용자 회원 가입을 진행하는 과정에서 해싱이 제대로 되지 않아 오류가 발생했지만 그대로 DB에 저장되는 상황이 발생.
# 이를 막기 위해서 트랜잭션 아토믹으로 valid를 통과한 이후에 트랜잭션을 추가해줌으로써 다음과 같은 오류 발생을 막음.
class SignUpView(APIView):

    def post(self, request):

        data = request.data
        password = request.data.get("password")
        db_user = User.objects.all()

        if db_user.filter(email = data["email"]).exists():
            return Response({"message":"이미 존재하는 이메일 입니다."})
        else:
            serializer = UserCreateSerializer(data=data)
            if serializer.is_valid():
                try:
                    with transaction.atomic():
                        user = serializer.save()
                        user.set_password(password)
                        user.save()
                        serializer = UserCreateSerializer(user)
                except Exception:
                    raise ParseError("비밀번호가 제대로 해싱되지 않았습니다.")
                
                return Response(serializer.data ,status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


# 사용자 비밀번호 변경
# 'User' object is not subscriptable
# 'User' object is not callable (objects라고 한해서 오류남;;)

'''
{
"old_password":123,
"new_password": 123123123}
'''

class ChangePassword(APIView):

    #email, password, old,newpassword

    def put(self, request , user_id):

        # 검증 넣어야함
        user = request.user
        old_password = request.data["old_password"]
        new_password = request.data["new_password"]
        if not old_password or not new_password:
            raise ParseError

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise

# 사용자 로그인

class LogInView(APIView):

    def post(self,request):
        username= request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            todo_category = TodoCategory.objects.all()
            if not todo_category.exists():

                challenge_category = [

                    {"name":"강아지 양치하기","discription":"하루 아침 혹은 저녁시간에 강아지 양치질을 합니다"},
                    {"name":"강아지 산책하기","discription":"하루 아침 혹은 저녁시간에 강아지와 산책을 합니다."},
                    {"name":"양치하기","discription":"강아지나 고양이의 권장 양치 횟수를 참고해서 양치질을 진행합니다."},
                    {"name":"사료 주기","discription":"하루 아침 혹은 저녁시간에 사료를 줍니다."},
                    {"name":"물 갈아주기","discription":"하루 아침 혹은 저녁시간에 깨끗한 물로 갈아줍니다."},
                    
                    ]
                
                todolist_category = [
                    {"author":user.pk ,"name" :"고양이 양치하기"} , 
                    {"author":user.pk ,"name" :"강아지 양치하기"} , 
                    {"author":user.pk ,"name" :"밥 주기"},
                    {"author":user.pk ,"name" :"물 갈아주기"},
                    {"author":user.pk ,"name" :"목욕 시키기"},
                    {"author":user.pk ,"name" :"산책 하기"},
                    {"author":user.pk ,"name" :"놀아 주기"},
                    ]
                
                todo_list = []
                for challenge in challenge_category:
                    challenge_serialzier = ChallengeCreateSerializer(data = challenge)
                    if challenge_serialzier.is_valid():
                        challenge_serialzier.save()
                    else:
                        return Response(challenge_serialzier.errors , status=status.HTTP_400_BAD_REQUEST)

                for category in todolist_category:
                    todo_serialzier = TodoCategorySerializer(data=category)
                    if todo_serialzier.is_valid():
                        todo_serialzier.save()
                        todo_list.append(todo_serialzier)
                        if len(todo_list) == 7 :
                            return Response({"message":"로그인 완료","discription":"카테고리 생성 완료"} , status=status.HTTP_201_CREATED)
                    else:
                        return Response({"message":"데이터 생성 시 에러발생"},status=status.HTTP_400_BAD_REQUEST)
                
            return Response({"message":"로그인 성공"}, status=status.HTTP_200_OK)
        else:
            return Response({"에러 발생":"아이디 혹은 비밀번호 오류입니다."}, status=status.HTTP_400_BAD_REQUEST)


# 사용자 로그아웃

class LogOutView(APIView):

    def post(self, request):
        logout(request)
        return Response({"로그아웃":"성공"}, status=status.HTTP_200_OK)


# JWT 로그인

# InvalidSignatureError: Signature verification failed : value에 잘못 데이터 넣음 ""따옴표 안뺌
# ValueError: Field 'id' expected a number but got 'user.pk'. 
# 잘되다가 반복적인 오류가 발 생했는데 , 토큰 발급하는 과정에서 헤더데이터에서 token을 안빼고 계속 발급해서 발생하는 오류였음, 헤더에 token을 빼고 다시 토큰을 발급받으니 잘됨

class JWTLogin(APIView):

    def post(self, request):

        username= request.data.get("username")
        password= request.data.get("password")

        if not username or not password:
            raise ParseError
        
        user = authenticate(request,username=username,password=password,)

        if user:
            token =jwt.encode({"pk":user.pk}, settings.SECRET_KEY,algorithm="HS256")
            return Response({"token":token} , status=status.HTTP_200_OK)
        
        else:
            return Response({"에러발생":"잘못된 정보를 입력하셨습니다."},status=status.HTTP_400_BAD_REQUEST)



# Simple JWT 회원가입
# 오류 떴지만 또 아이디 지맘대로 생김 ;;;;

# Simpe JWT 토큰을 발행하는 로그인 기능.
# 일반 로그인 기능과 마찬가지로 오류가 발생했지만 DB에 저장되는 경우가 발생함
# transaction.atomic()으로 해싱 오류가 발생 시 콜백 진행
class RegisterAPIView(APIView):

    def post(self, request):

        data = request.data
        password = request.data.get("password")
        db_user = User.objects.all()

        if db_user.filter(email = data["email"]).exists():
            return Response({"message":"이미 존재하는 이메일 입니다."})
        else:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                        try:
                            with transaction.atomic():
                                user = serializer.save()
                                user.set_password(password)
                                user.save()
                                token = TokenObtainPairSerializer.get_token(user)
                                refresh_token = str(token)
                                res = Response({
                                    "user":serializer.data,
                                    "message":"register success",
                                    "token":{
                                    "refresh":refresh_token,
                                    },
                                },
                                status=status.HTTP_200_OK,
                                )
                                return res
                        except Exception:
                            raise ParseError("비밀번호가 해싱되는 과정에서 오류가 발생했습니다. 다시 시도해주세요.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Simple Jwt 로그인
# 토큰틀 cookie에 저장함

class SimpleJwtLoginView(APIView):

    def post(self, request):
        
        user = authenticate(request,username=request.data.get("username"),password=request.data.get("password"))
        
        if user is not None:
            serializer = SimpleJWTLoginSerialzier(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token =str(token)
            access_token = str(token.access_token)
            res = Response({

                "user" : serializer.data,
                "message":"login Success",
                "token":{
                "access":access_token,
                "refresh":refresh_token,
                },
            },
                status=status.HTTP_200_OK,
            )
            res.set_cookie(key="refreshtoken",value=refresh_token,httponly=True)
            res.set_cookie(key="accesstoken",value=access_token,httponly=True)
            return res
        else:
            return Response({"message":"로그인 오류"},status=status.HTTP_400_BAD_REQUEST)

class SimpleJWTLogOutView(APIView):
    def post(self, request):

        response = Response({
            "message":"Logout Success"
        },status=status.HTTP_200_OK
        )
        response.delete_cookie("refreshtoken")
        return response

# 소셜 로그인 

# 소셜 회원가입

