from django.db.models import Q
from django.core.paginator import Paginator

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404 , ListAPIView 
from rest_framework.response import Response 
from rest_framework.pagination import PageNumberPagination 

from contents.models import Content , Comment , Category 

from contents.serializers import ContentListView , CommentSerializer ,CommentCreateSerializer , ContentCreateSerializer , CategorySerializer ,ContentDetailSerializer

from rest_framework.viewsets import ModelViewSet

# Create your views here.



# 운영자가 제공하는 콘텐츠 전체 뷰

class ConetntView(APIView):

    def get(self, request):
        all_contents = Content.objects.all()
        serializer = ContentListView(all_contents, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)

class ContentCreateView(APIView):

    def post(self ,request, user_id ):

        request_data_copy= request.data.copy()
        datas=request_data_copy
        datas.update({"author":user_id})
        serializer = ContentCreateSerializer(data=datas)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data ,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


# 콘텐츠 조회 / 수정 / 삭제
class ContentDetailView(APIView):

    # 게시글 조회수 기능은 새로고침이 발생하면 계속해서 증가하는 문제가 있습니다.
    # 같은 사용자일 경우 조회수 증가를 하지 못하는 방법을 고안해야 할 것 같습니다.
    def get(self, request, content_id):
        
        content = Content.objects.get(id=content_id)
        content.contents_view = content.contents_view + 1
        content.save()
        serializer = ContentDetailSerializer(content)
        return Response(serializer.data)

    def put(self,request, content_id):

        request_data_copy= request.data.copy()
        datas=request_data_copy
        datas.update({"author":request.user.id})
        content = Content.objects.get(id=content_id)
        serialzier = ContentCreateSerializer(content , data=datas , partial=True)
        if serialzier.is_valid():
            serialzier.save()
            return Response(serialzier.data ,status=status.HTTP_200_OK)
        else:
            return Response(serialzier.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, content_id):
        content = Content.objects.get(id=content_id)
        if request.user == content.author:
            content.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


# 콘텐츠 좋아요

class ContentsLikeView(APIView):

    def post(self, request, content_id):
        content = Content.objects.get(id=content_id)
        if request.user in content.likes.all():
            content.likes.remove(request.user)
            content.save()
            return Response({"message":"좋아요 취소"},status=status.HTTP_200_OK)
        
        else:
            content.likes.add(request.user)
            content.save()
            return Response({"message":"좋아요 "},status=status.HTTP_200_OK)

    

# 콘텐츠 댓글 뷰
class CommentView(APIView):

    def get(self, request, content_id):
        # 해당 콘텐츠 불러오기
        content = Content.objects.get(id=content_id)
        # 해당 콘텐츠에 속한 댓글 불러오기
        comments = content.comment_set.all()
        serializers = CommentSerializer(comments, many=True)

        return Response(serializers.data , status=status.HTTP_200_OK)

    def post(self, request, content_id):
        
        request_data_copy= request.data.copy()
        datas=request_data_copy
        datas.update({"author":request.user.id , "content":f"{content_id}"})
        print(datas)
        if len(datas) == 3:
            serializer = CommentCreateSerializer(data=datas)
            if serializer.is_valid():
                comments = serializer.save(author=request.user, content_id=content_id)
                serializer = CommentCreateSerializer(comments)
                return Response(serializer.data , status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"댓글을 입력해주세요"} , status=status.HTTP_400_BAD_REQUEST)

        
# 댓글 조회/ 수정 / 삭제
class CommentDetailView(APIView):

    def get(self,request, content_id, comment_id):
        content = Content.objects.get(id=content_id)
        comment = content.comment_set.get(id=comment_id)
        serialzier = CommentSerializer(comment)
        return Response(serialzier.data , status=status.HTTP_200_OK)

    def put(self,request, content_id, comment_id):  
        comment = Comment.objects.get(id=comment_id)

        if request.user == comment.author:
            serialzier = CommentCreateSerializer(comment, data=request.data, partial=True)
            if serialzier.is_valid():
                serialzier.save()
                return Response(serialzier.data , status=status.HTTP_200_OK)
            else:
                return Response(serialzier.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("수정 권한이 없습니다." , status=status.HTTP_401_UNAUTHORIZED)        

    def delete(self,request, content_id, comment_id):
        comment = Comment.objects.get(id=comment_id)
        if request.user == comment.author:
            comment.delete()
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("삭제 권한이 없습니다.", status=status.HTTP_401_UNAUTHORIZED)



# 카테고리
# class TestViewSet(APIView):

#     def get(self, request, category_name):
        
#         category = get_object_or_404(Category, name=category_name)
#         print(category)
#         content = Content.objects.filter(Q(categories__id__contains=category.pk))
#         print(content)
#         serialzier = ContentSerializer(content, many=True)
#         return Response(serialzier.data)


# TEST

class setPagination(PageNumberPagination):
    page_size = 3

class TestViewSet(ListAPIView):

    queryset=Content.objects.all()
    serializer_class = ContentListView
    pagination_class = setPagination
    filter_backends = (SearchFilter,)
    search_fields = ("categories__name",)

class CategoryView(APIView):
    def get(self, reuqest):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryDetailView(APIView):
    
    def get(self ,request ,category_id):
        category = Category.objects.get(pk=category_id)
        serializer = CategorySerializer(category)
        return Response(serializer.data , status=status.HTTP_200_OK)