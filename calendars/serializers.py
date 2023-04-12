from rest_framework import serializers
from calendars.models import ToDoList,  Challenge , UserChallenge ,TodoCategory 


# ToDo Category

class ToDoCategoryViewSerializer(serializers.ModelSerializer):

      author = serializers.SerializerMethodField()

      def get_author(self,obj):
            return obj.author.username
      
      class Meta:
            model = TodoCategory
            fields= ["pk","author","name"]

# 투두 생성

class TodoCategorySerializer(serializers.ModelSerializer):
      
      class Meta:
            model = TodoCategory
            fields = ["pk","author" ,"name"]

# 투두 리스트 리스트
class ToDoListSerializer(serializers.ModelSerializer):
        
      author = serializers.SerializerMethodField()
      title = serializers.SerializerMethodField()

      def get_author(self, obj):
            return obj.author.username

      def get_title(self,obj):
            return obj.title.name

      class Meta:
            model = ToDoList
            fields = ["pk","discription","author","title","is_works","date","update_date"]

# 투두 리스트 상세

class ToDoListDetailSerializer(serializers.ModelSerializer):

      class Meta:
            model = ToDoList
            fields = ["pk","discription","author","title","is_works","date","update_date"]


class ToDoCreateSerializer(serializers.ModelSerializer):
      
      class Meta:
            model = ToDoList
            fields = ["author", "title", "discription","date"]

# 챌린지 목록 조회회

class ChallengeSerializer(serializers.ModelSerializer):

        class Meta:
            model = Challenge
            fields = ["pk","name","discription","image"]

# 챌린지 생성

class ChallengeCreateSerializer(serializers.ModelSerializer):

      class Meta:
            model = Challenge
            fields = ["name","discription",]

# 유저 챌린지 

class UserChallengeSerializer(serializers.ModelSerializer):

        class Meta:
            model = UserChallenge
            fields = ["users","mychallenge"]

# 유저 별 챌린지 상세페이지

class UserChallengeDetailSerializer(serializers.ModelSerializer):

      users = serializers.SerializerMethodField()
      mychallenge = serializers.SerializerMethodField()

      def get_mychallenge(self,obj):
            return obj.mychallenge.name

      def get_users(self,obj):
        return obj.users.username

      class Meta:
            model = UserChallenge
            fields = ["pk","users","mychallenge","today_is_work","complete","count","created_date","updated_date" ]



class UserChallengeListSerializer(serializers.ModelSerializer):

      users = serializers.SerializerMethodField()
      mychallenge = serializers.SerializerMethodField()

      def get_mychallenge(self,obj):
            return obj.mychallenge.name

      def get_users(self,obj):
        return obj.users.username

      class Meta:
            model = UserChallenge
            fields = ["pk", "users","today_is_work","complete","count","created_date","updated_date","mychallenge"]

