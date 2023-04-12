from django.test import TestCase
from rest_framework.test import APITestCase

from contents.models import Category , Comment , Content
from users.models import User
from calendars.models import Challenge , TodoCategory, ToDoList ,UserChallenge
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.


class TestToDoList(APITestCase):


    TODOLIST_CATEGORY_NAME = "고양이 밥주기"

    TODOLIST_DAYS = "2023-04-01"

    def setUp(self):


        # 회원 가입
        signup_data={
            "email":"admin1@admin.com",
            "password":"123"
        }
        signup_response = self.client.post("/users/signup/",data=signup_data)
        
        # 로그인
        data={
            "username":"admin1@admin.com",
            "password":"123",
        }
        login_response = self.client.post("/users/login/",data=data)
        
        # 생성 유저 조회
        user_response = self.client.get("/users/me/")
        user_data = user_response.json()
        self.user_pk=user_data["pk"]

        # 체크리스트 카테고리 생성

        category_data={
            "name" : self.TODOLIST_CATEGORY_NAME,
        }

        category_response = self.client.post(f"/calendar/{self.user_pk}/todolist/create/", data=category_data)
        create_data = category_response.json()
        self.category_pk = create_data["pk"]

        # 날짜별 체크리스트 생성
        day_data={
            "title":self.category_pk,
            "discription" :"일어나면 밥먹고 고양이 밥주기",
        }
        day_response =self.client.post(f"/calendar/{self.user_pk}/todolist/detail/{self.TODOLIST_DAYS}/",data=day_data)
        
        self.assertEqual(day_response.status_code,201,"체크리스트 생성 실패")
        
        # 체크리스트 날짜별 조회
        todo_pk_response = self.client.get(f"/calendar/{self.user_pk}/todolist/detail/{self.TODOLIST_DAYS}/")
        
        self.assertEqual(todo_pk_response.status_code,200,"날짜별 체크리스트 조회 실패")

        # 자기 자신 조회
    def test_get_me(self):

        response = self.client.get("/users/me/")
        user_data = response.json()

        # 체크리스트 카테고리 생성
    def test_create_todolist_category(self):

        data={
            "name" : self.TODOLIST_CATEGORY_NAME,
            "author" : self.user_pk
        }

        response = self.client.post(f"/calendar/{self.user_pk}/todolist/create/", data=data)
        create_data = response.json()
        
        self.assertEqual(response.status_code,200,"카테고리 생성 실패")
        self.assertEqual(create_data["name"],self.TODOLIST_CATEGORY_NAME)


        #사용자가 작성한 카테고리 조회
    def test_get_todolist_category(self):

        response = self.client.get(f"/calendar/{self.user_pk}/todolist/category/")
        data = response.json()

        self.assertEqual(response.status_code,200,"카테고리 조회 실패")

        #날짜별 체크리스트 생성
    def test_create_todolist(self):

        data={
            "title":self.category_pk,
            "discription" :"일어나면 밥먹고 고양이 밥주기",
        }
        response =self.client.post(f"/calendar/{self.user_pk}/todolist/detail/{self.TODOLIST_DAYS}/",data=data)

        self.assertEqual(response.status_code,201,"체크리스트 생성 실패")

        #날짜별 체스리스트 조회
    def test_get_todolist(self):

        response = self.client.get(f"/calendar/{self.user_pk}/todolist/detail/{self.TODOLIST_DAYS}/")


        self.assertEqual(response.status_code,200,"날짜별 체크리스트 조회 실패")

        #체크리스트 완료 여부
    def test_check_todolist(self):

        response = self.client.post(f"/calendar/{self.user_pk}/todolist/day/{self.TODOLIST_DAYS}/detail/{1}/work/")

        self.assertEqual(response.status_code,200,"체크 유무 과정에서 에러 발생")

        #체크리스트 수정
    def test_put_todolist(self):
        data={
            "title":self.category_pk,
            "discription" :"수정 테스트",
            "date":self.TODOLIST_DAYS
        }
        response = self.client.put(f"/calendar/{self.user_pk}/todolist/day/1/detail", data=data)

        self.assertEqual(response.status_code,200,"체크리스트 수정 실패")

        #체크리스트 삭제
    def test_delete_todolist(self):

        response = self.client.delete(f"/calendar/{self.user_pk}/todolist/day/1/detail")

        data = response.status_code

        self.assertEqual(response.status_code,404,"체크리스트 삭제 실패")

class TestChallenge(APITestCase):

    def setUp(self): 

        # 회원 가입
        signup_data={
            "email":"admin1@admin.com",
            "password":"123"
        }
        signup_response = self.client.post("/users/signup/",data=signup_data)
        
        # 로그인
        data={
            "username":"admin1@admin.com",
            "password":"123",
        }
        login_response = self.client.post("/users/login/",data=data)
        
        # 생성 유저 조회
        user_response = self.client.get("/users/me/")
        user_data = user_response.json()
        self.user_pk=user_data["pk"]


        # 챌린지 도전하기(생성하기)

        # post_challenge_response = self.client.post(f"/calendar/challenge/create/{self.user_pk}/")
        

        # 유저가 진행중인 챌린지
        # user_challenge_response = self.client.get(f"/calendar/challenge/mychallenge/{self.user_pk}")
        # testcodes = user_challenge_response.json()


        #챌린지 리스트 전체 조회
    def test_get_challengelist(self):

        response = self.client.get("/calendar/challenge/")

        self.assertEqual(response.status_code,200,"챌린지 전체 조회 실패")

        #챌린지 상세 조회
    def test_get_challengeDetail(self):
        
        response = self.client.get("/calendar/challenge/1/")
        
        self.assertEqual(response.status_code,200,"챌린지 상세 페이지 조회 실패")

        # 챌린지 도전하기 (생성하기)
    def test_post_challenge(self):

        data = {
            "mychallenge": 1
        }
        response = self.client.post(f"/calendar/challenge/create/{self.user_pk}/",data=data)

        self.assertEqual(response.status_code,201,"이미 진행중인 챌린지 입니다.")
        

        # 도전중인 챌린지 상세 조회
    def test_get_userchallengedatail(self):
        
        response = self.client.get(f"/calendar/challenge/user/{self.user_pk}/challenge/1/")

        self.assertEqual(response.status_code,200,"해당 챌린지를 조회할 수 없습니다.")

        # 도전중인 챌린지 오늘 완료!!!
    def test_post_userchallengedetail(self):

        response =self.client.post(f"/calendar/challenge/user/{self.user_pk}/detail/1/")

        self.assertEqual(response.status_code,200,"오늘 챌린지를 이미 완료했습니다")

        # 도전중인 챌린지 삭제!
    def test_delete_userchallengedetail(self):
        
        response = self.client.delete(f"/calendar/challenge/user/{self.user_pk}/detail/1/")

        self.assertEqual(response.status_code,404,"삭제에 실패했습니다.")