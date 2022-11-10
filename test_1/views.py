from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.db.models import Q
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework.filters import SearchFilter
from rest_framework import filters
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie ,Genre
from .serializers import MovieTitleSerializer ,MovieDetailSerializer, GenreSerializer

from movies.modles import Movie
from rest_framework.views import APIView
from rest_framework import status
from movies.models import Comment
from movies.serializers import CommentSerializer
from movies.serializers import CommentCreateSerializer

# 22.11.06 최신욱 추가.

# 영화 리스트 전체
class movie_list(ListAPIView):
    queryset = Movie.objects.all()
    movie_lists = get_list_or_404(Movie)
    serializer_class = MovieTitleSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    #filterset_fileds = ['title', 'original_title', 'genres']
    search_fields =  ['title', 'original_title', 'genres']
    


##무비 상세정보 페이지
@api_view(['GET'])
def movie_detail(request, movie_pk ):
    movie = get_object_or_404(Movie, pk=movie_pk)
    genre = movie.genres.all()
    serializer = MovieDetailSerializer(movie)
    serializer2 = GenreSerializer(genre, many=True)
    return Response([serializer.data, serializer2.data])

# 평점이 7점 이상인 영화들만 불러오기
@api_view(['GET']) 
def vote_average(request):
    movies = Movie.objects.filter(vote_average__gte=7.0)
    serializer = MovieDetailSerializer(movies, many=True)
    return Response(serializer.data)


#장르별 리스트 출력
@api_view(['GET'])
def genre_list(request, genre_name):
    genre = get_object_or_404(Genre, name=genre_name)
    movies = Movie.objects.filter(Q(genres__id__contains=genre.pk))
    serializer = MovieDetailSerializer(movies, many=True)
    return Response(serializer.data)
    



#박소민_댓글기능 추가
class CommentView(APIView):
    def get(self, request, movie_pk):
        post = Comment.objects.all()
        serializer = CommentSerializer(post, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, movie_pk):
        print(request.user)
        serializers = CommentCreateSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save(user=request.user, movie_id=movie_pk)
            return Response(serializers.data)
        else:
            return Response(serializers.errors)

    

class CommentDetailView(APIView): #20221107 문규빈 댓글 수정 / 삭제
    def put(self, request, comment_id): # 댓글 수정
        comment = get_object_or_404(Comment, id=comment_id)
        print(request.user,comment.user)
        if request.user == comment.user:  #문규빈 / 작성자만 수정 가능하게 하는 코드   
            serializers = CommentCreateSerializer(comment, data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_200_OK)
            else:
                return Response(serializers.erros, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN) # 문규빈 / 작성자가 아닐경우 에러코드 전송
    
    def delete(self, request, comment_id): #댓글 삭제
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN) 
