from django.shortcuts import render

# Create your views here.
from django.db.models import Q

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response 

from users.models import User
from calendars.models import TodoCategory ,ToDoList  ,UserChallenge ,Challenge
from calendars.serializers import  ToDoListSerializer, ToDoCreateSerializer, ChallengeSerializer, UserChallengeSerializer ,  UserChallengeSerializer ,UserChallengeSerializer ,ToDoListDetailSerializer ,TodoCategorySerializer ,UserChallengeListSerializer ,ToDoCategoryViewSerializer ,UserChallengeDetailSerializer
import datetime 


# ToDoList category List View

class ToDoListCategoryView(APIView):

    def get(self,request,user_id):

        user = User.object.get(id=user_id)
        category = TodoCategory.objects.filter(author=user)
        if category:
            serialzier = ToDoCategoryViewSerializer(category, many=True)
            return Response(serialzier.data,status=status.HTTP_200_OK)
        else:
            return Response({"message":"현재 저장된 카테고리가 없습니다."})



# 사용자가 작성한 ToDoList (체크리스트) 조회

class TodoListAllView(APIView):

    def get(self,request, user_id):

        user = User.objects.get(id=user_id)
        if user:
            user_todolist = ToDoList.objects.filter(author=user)

            if user_todolist:
                serialzier = ToDoListSerializer(user_todolist,many=True)
                return Response(serialzier.data , status=status.HTTP_200_OK)
            else:
                return Response({"message":"조회할수 없습니다."})
        else:
            return Response({"message":"사용자가 없습니다."})

# ToDoCategory 생성

class TodoCategoryCreate(APIView):
    def post(self, request ,user_id):
        
        request_data_copy= request.data.copy()
        datas=request_data_copy   
        datas.update({"author":request.user.id})
        serializer = TodoCategorySerializer(data=datas)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# 사용자가 해야 할 목록 날짜별 조회/생성 
class ToDoListView(APIView):

    def get(self,request , todo_day , user_id):

        todos = ToDoList.objects.filter(date=todo_day)
        serializer = ToDoListSerializer(todos, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)

    def post(self,request ,todo_day,user_id):

        request_data_copy= request.data.copy()
        datas=request_data_copy
        datas.update({"author":request.user.id , "date":todo_day})
        serializer = ToDoCreateSerializer(data=datas)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data ,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)



# 불리안 필드는 update함수가 없어서 동작을 안함
# 그래서 save를 통해서 입력값을 넣어주어야 합니다.
# 체크여부확인
class ToDolistWorkView(APIView):

    def post(self, request, todo_id, todo_day , user_id):
        todos = ToDoList.objects.get(id=todo_id)
        if todos.is_works is False:
            todos.is_works = True
            todos.save()
            return Response(status=status.HTTP_200_OK)
        else:
            todos.is_works = False
            todos.save()
            return Response(status=status.HTTP_200_OK)


# 해야 할 목록 조회/ 수정 / 삭제
class ToDoListDetailView(APIView):
        
        def get(self, request, todo_id, user_id):
            todos = ToDoList.objects.get(id=todo_id)
            serialzier = ToDoListDetailSerializer(todos)
            return Response(serialzier.data)

        def put(self, request, todo_id, user_id):
            todos = ToDoList.objects.get(id=todo_id)
            request_data_copy= request.data.copy()
            datas=request_data_copy
            datas.update({"author":request.user.id})

            serializer = ToDoCreateSerializer(todos , data=datas)
            if serializer.is_valid():
                serializer.save()    
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        
        def delete(self, request, todo_id, user_id ):

            todos = ToDoList.objects.get(id=todo_id)
            if request.user == todos.author:
                todos.delete()
                return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response("삭제 권한이 없습니다.", status=status.HTTP_401_UNAUTHORIZED)


# 도전할 챌린지 전체 리스트 목록 / 조회
class ChallengeListView(APIView):

    def get(self, request):
        challenge =  Challenge.objects.all()
        serializer = ChallengeSerializer(challenge, many=True)
        return Response(serializer.data)

        

        
# 챌린지 디테일 페이지

class ChallengeDetailView(APIView):

    def get(self, request, challenge_id):
        challenge = Challenge.objects.get(id=challenge_id)
        serializer = ChallengeSerializer(challenge)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 챌린지 도전하기
class UserCreateChallengeView(APIView):    

    def post(self,request,user_id):

        # request_data_copy = request.data.copy() # mutable 한 딕셔너리로 카피하는 메서드
		# 		request_data_copy['user'] = request.user.id

        request_data_copy= request.data.copy()
        datas=request_data_copy
        datas.update({"users":request.user.id})
        print(datas)

        if len(datas) == 2:
            userchallenge = UserChallenge.objects.filter(users=user_id)
            serialzier = UserChallengeSerializer(data=datas)
            if not userchallenge.filter(mychallenge=datas["mychallenge"]).exists():
                if serialzier.is_valid():
                    serialzier.save()
                    return Response(serialzier.data , status=status.HTTP_201_CREATED)
                else:
                    return Response(UserChallengeSerializer.errors , status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message":"이미 진행하는 챌린지입니다."} , status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"입력데이터가 부족합니다."})
    
        
    # def post(self, request , user_id):
    #     # createSeraizleir 로 변경해야함

    #     userchallenge = UserChallenge.objects.filter(users_id=user_id)
    #     if request.user.userchallenge_set.name not in userchallenge.name:
    #         datas = request.data
    #         datas.update({"users":request.user.id})
    #         serialzier = UserChallengeSerializer(data=datas)
    #         if serialzier.is_valid():
    #             serialzier.save()
    #             return Response(serialzier.data , status=status.HTTP_200_OK)
    #         else:
    #             return Response(serialzier.errors, status=status.HTTP_404_NOT_FOUND)
            
    #     else:
    #         return Response("이미 진행중인 챌린지 입니다. " , status=status.HTTP_400_BAD_REQUEST)


# 챌린지 디테일페이지 조회

class UserChallengeDetailPageView(APIView):

     def get(self,request,user_id , userchallenge_id):
        userchallenge = UserChallenge.objects.get(mychallenge = userchallenge_id)
        reset_time = datetime.datetime.now().date()

        # test = "2023-03-22"
        # test_day = datetime.datetime.strptime(test,"%Y-%m-%d").date()
        if request.user == userchallenge.users:
            serialzier = UserChallengeDetailSerializer(userchallenge)
            if userchallenge.updated_date < reset_time:
                userchallenge.today_is_work = False
                userchallenge.save() 

                return Response(serialzier.data , status=status.HTTP_200_OK)
            
            return Response(serialzier.data , status=status.HTTP_200_OK)
        else:
            return Response("권한 없는 접근 입니다.", status=status.HTTP_401_UNAUTHORIZED)


# 도전 중인 챌린지 수정/삭제(초기화)

class UserChallengeDetailView(APIView):

    def post(self, request, user_id, userchallenge_id):
        userchallenge = UserChallenge.objects.get(mychallenge = userchallenge_id)

        if request.user == userchallenge.users:
            if userchallenge.today_is_work is False:
                userchallenge.today_is_work = True
                userchallenge.count += 1
                userchallenge.save()
                return Response({"message":"오늘 챌린지 완료!!"} , status=status.
            HTTP_200_OK)

            else:
                return Response({"message":"오늘 챌린지는 이미 완료했습니다."} , status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message":"권한이 없습니다."},status=status.HTTP_401_UNAUTHORIZED)


    def delete(self, request,user_id, userchallenge_id):
        userchallenge = UserChallenge.objects.get(id=userchallenge_id)
        if request.user == userchallenge.users:
            userchallenge.delete()
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("권한이 없습니다." , status=status.HTTP_401_UNAUTHORIZED)


class MyChallengeListView(APIView):

    def get(self, reuqest, user_id):
        mychallenge = UserChallenge.objects.filter(users=user_id)
        serializer = UserChallengeListSerializer(mychallenge, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
