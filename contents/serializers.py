from rest_framework import serializers
from contents.models import Content , Comment ,Category 
from users.serializers import TinyUserSerializer



# 댓글 리스트      
class CommentSerializer(serializers.ModelSerializer):
    author = TinyUserSerializer()

    # author = serializers.SerializerMethodField()

    # def get_author(self,obj):
    #     return obj.author.username
    
    class Meta:
        model = Comment
        fields = ["pk" ,"discription","author","content","create_date","update_date"]

# 댓글 작성하기
class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ["content","author","discription"]
#  데이터 생성이 안되서 도대체 왜 dB에 안쌓이지? 확인해보니 시리얼라이저에서 안받아주고 잇었음;;


# 카테고리 리스트
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["pk", "name"]

#  이미지
# class ImageSerializer(serializers.ModelSerializer):

#     # content = serializers.SerializerMethodField()

#     # def get_content(self,obj):
#     #     return obj.content.title

#     class Meta:
#         model = ImageModel
#         fields = ["pk", "image" , "content"]


# 게시글 상세
class ContentDetailSerializer(serializers.ModelSerializer):
    # images = ImageSerializer(many=True)
    comment_set = CommentSerializer(many=True)

    author = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author.username
    
    def get_categories(self, obj):
        return obj.categories.name
    
    def get_likes(self,obj):
        return obj.likes.count()
    

    class Meta:
        model = Content
        fields = ["title","discription","author","categories","likes","created_date","updated_date" , "images","comment_set"]

# 게시글 리스트
class ContentListView(serializers.ModelSerializer):
    # images = ImageSerializer(many=True)

    author = serializers.SerializerMethodField()
    categories =serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author.username
    
    def get_categories(self,obj):
        return obj.categories.name
    
    def get_likes(self, obj):
        return obj.likes.count()

    class Meta:
        model = Content
        fields = ["pk", "title","discription","author","categories","likes","created_date","updated_date" , "images"]

# 게시글 생성 / 추후 이미지도 넣을 수 있으면 좋을 듯
class ContentCreateSerializer(serializers.ModelSerializer):
    # images = ImageSerializer(read_only=True, many=True)

    class Meta:
        model = Content
        fields = ["title","discription","author" ,"categories" ,"images"]

    # def create(self,validated_data):
    #     image_data = self.context["request"]
    #     print("이미지데이터",image_data)
    #     instance = Content.objects.create(**validated_data)
    #     print("포스터데이터",instance)
    #     for image_data in image_data.getlist("images"):
    #         ImageModel.objects.create(post=instance , images=image_data)
    #     return instance