from django.test import TestCase
from rest_framework.test import APITestCase

from contents.models import Category , Comment , Content
from users.models import User
from calendars.models import Challenge , TodoCategory, ToDoList ,UserChallenge
from django.core.files.uploadedfile import SimpleUploadedFile




class TestUser(APITestCase):

        TEST_USERNAME ="사용자 이름 테스트"
        TEST_IMAGE =test_image = SimpleUploadedFile(name='test_image.png', content=b'', content_type='image/png')

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

        # 회원가입
        def test_signup(self):

                signup_data={
                "email":"admin1@admin.com",
                "password":"123"
                }
                response = self.client.post("/users/signup/",data=signup_data)

                self.assertEqual(response.status_code,200,"회원 가입 실패")

        # 로그인
        def test_login(self):

                data={
                "username":"admin1@admin.com",
                "password":"123",
                }
                response = self.client.post("/users/login/",data=data)
                
                self.assertEqual(response.status_code,200,"로그인 실패")

        # 사용자 자기 자신 정보 조회
        def test_get_user(self):

                response =self.client.get("/users/me/")

                self.assertEqual(response.status_code,200,"개인 정보 조회 실패")

        # 개인정보수정
        def test_put_user(self):
                
                #이미지 파일이 비어있다고 합니다...?

                data={
                        "username":self.TEST_USERNAME,
                        # "profile_img":self.TEST_IMAGE
                }

                response = self.client.put(f"/users/profile/{self.user_pk}/",data=data)

                self.assertEqual(response.status_code,200,"회원 정보 수정 실패")
        
        # 회원탈퇴
        def test_delete_user(self):

                response = self.client.delete(f"/users/profile/{self.user_pk}/")

                self.assertEqual(response.status_code,204,"회원 탈퇴 실패")

        # 로그아웃
        def test_logout_user(self):

                response = self.client.post(f"/users/logout/")
                self.assertEqual(response.status_code,200,"로그아웃 실패")

        # simple jwt 로그인
        def test_simplejwt_login(self):

                data = {
                        "username":"admin1@admin.com",
                        "password":"123", 
                }
                response = self.client.post(f"/users/api/register/login/",data=data)
                
                self.assertEqual(response.status_code,200, "simple jwt 로그인 실패")
        
        # simple jwt 로그아웃
        def test_simplejwt_logout(self):

                response = self.client.post(f"/users/api/register/logout/")

                self.assertEqual(response.status_code,200,"simple jwt 로그아웃 실패")