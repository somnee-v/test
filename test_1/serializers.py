from rest_framework import serializers
from .models import  Movie ,Genre
from .models import Comment


# 22.11.06 최신욱 추가.

#무비 id와 타이틀
class MovieTitleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = ('id', 'title','poster_path','genres', 'original_title')

# 영화 데이터 전체 API
class MovieDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = "__all__"

# 장르
class GenreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Genre
        fields = '__all__'

# 댓글
class CommentSerializer(serializers.ModelSerializer):
    # users = serializers.ReadOnlyField(source = 'users.email')
    class Meta:
        model = Comment
        fields = '__all__'
        
class CommentCreateSerializer(serializers.ModelSerializer):
    # users = serializers.ReadOnlyField(source = 'users.email')
    class Meta:
        model = Comment
        fields = ['content']