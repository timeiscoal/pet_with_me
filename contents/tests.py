from django.test import TestCase
from rest_framework.test import APITestCase

from contents.models import Category , Comment , Content
from users.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


# Create your tests here.

class TestCategory(APITestCase):

    CATEGORY_NAME = "테스트 카테고리"
    GET_CATEGORY_URL = "/content/api/v3/category/"


    def setUp(self):
        Category.objects.create(name=self.CATEGORY_NAME)

    def test_all_categories(self):
        response = self.client.get(self.GET_CATEGORY_URL)
        data= response.data
        self.assertEqual(response.status_code,200,"상태 코드 200이 아닙니다")
        self.assertEqual(len(data),1,)
        self.assertIsInstance(data,list,)
        self.assertEqual(data[0]["name"], self.CATEGORY_NAME)


class TestContent(APITestCase):

    CATEGORY_NAME = "고양이 카테고리"
    CONTENT_TITLE = "게시글 테스트"
    CONTENT_DISCRIPTION = "게시글 내용 테스트"
    COMMENT_DISCRIPTION = "댓글 내용 테스트"

    GET_CONTENT_URL = "/content/api/v1/"

    GET_CATEGORY_CONTENT_URL = "/content/api/v3/categorylist/"
    SEARCH_URL = "?search=고양이"

    POST_CREATE_CONTENT = "/content/api/v1/conetnt/create/"
    
    # 게시글 초기 값 설정
    def setUp(self):

        user = User.objects.create(username="admin@admin.com")
        user.set_password("123")
        user.save()

        self.test_user = user
        self.test_category = Category.objects.create(name=self.CATEGORY_NAME)
        self.test_image = SimpleUploadedFile(name='test_image.png', content=b'', content_type='image/png')
        
        self.test_content = Content.objects.create(
            title=self.CONTENT_TITLE, 
            discription=self.CONTENT_DISCRIPTION,
            author=self.test_user , 
            categories=self.test_category ,
            images=self.test_image,
            )
        
        self.test_comment = Comment.objects.create(
            author = self.test_user,
            content = self.test_content,
            discription = self.COMMENT_DISCRIPTION,
        )

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

    # 자기 자신 조회
    def test_get_me(self):

        response = self.client.get("/users/me/")
        self.data = response.json()   

    # 게시글 전체 조회
    def test_all_contents(self):
        
        response = self.client.get(self.GET_CONTENT_URL)
        data = response.json()
        
        self.assertEqual(response.status_code,200,"게시글 전체 조회 실패")
        
    
    # 카테고리별 게시글 조회
    def test_category_contents(self):

        response = self.client.get(self.GET_CATEGORY_CONTENT_URL+self.SEARCH_URL)
        data=response.json()

        self.assertEqual(response.status_code,200,"카테고리별 게시글 조회 실패")
        self.assertEqual(data["results"][0]["author"],self.test_user.username)

    # 게시글 생성

    def test_create_contents(self):

        # 이미지가 계속 들어가긴 하나 빈값이라고 하는 이유가 무엇일까?
        data = {
            "title":"생성 테스트 제목", 
            "discription":"생성 테스트 내용",
            "categories": 1,
            # "images": self.test_image
        }

        response = self.client.post(f"/content/api/v1/conetnt/create/{self.test_user.pk}/" , data=data)
        create_data = response.json()
        
        self.assertEqual(response.status_code,201,"게시글 생성 실패")
        self.assertEqual(create_data["author"],self.test_user.pk)
        self.assertEqual(create_data["categories"],self.test_category.pk)

    # 게시글 수정
    def test_put_contents(self):

        data = {
            "title":"생성 테스트 제목", 
            "discription":"생성 테스트 내용",
            "categories": 1,
            # "images": self.test_image
        }

        response = self.client.put(f"/content/api/v2/{self.test_content.pk}/", data=data)
        put_data = response.json()

        self.assertEqual(response.status_code,200,"게시글 수정 실패")

    # 게시글 좋아요
    def test_like_content(self):

        response= self.client.post(f"/content/api/v2/{self.test_content.pk}/like/")

        self.assertEqual(response.status_code,200,"좋아요 및 취소 실패")

    # 댓글 조회
    def test_get_comment(self):

        response = self.client.get(f"/content/api/v2/{self.test_content.pk}/comment/")
        data = response.json()
        
        self.assertEqual(response.status_code,200,"댓글 불러오기 실패")

    # 댓글 생성
    def test_post_comment(self):

        data={
            "content" : self.test_content.pk ,
            "discription": "안녕하세요",
        }

        response = self.client.post(f"/content/api/v2/{self.test_content.pk}/comment/", data=data)
        comment_data=response.json()

        self.assertEqual(response.status_code,200,"댓글 작성 실패")

    # 댓글 삭제
    def test_delete_comment(self):
        response = self.client.get(f"/content/api/v2/1/comment/1/")
        comment_data=response.json()

    