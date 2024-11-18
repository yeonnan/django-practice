from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from posts.models import Post
from posts.serializers import PostSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

class PostListAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]       # 인증된 사용자만 수정가능, 읽기는 인증 없이도 가능
    # 게시판 조회
    def get(self, request):
        posts = Post.objects.all()      # 모든 Post 객체를 가져옴
        serializer = PostSerializer(posts, many=True)       # 여러개의 Post 객체 직렬화 (many=True)
        return Response(serializer.data)
    
    # 게시글 생성
    def post(self, request):
        # 클라이언트의 요청 데이터를 PostSerializer로 직렬화, context에 request 추가
        # data=request.data : 클라이언트가 보낸 데이터를 직렬화 클래스에 전달하는 역할
        # context : 직렬화 클래스에 정보를 전달할 수 있는 딕셔너리. context에 담긴 정보는 직렬화 클래스 내부에서 self.context로 접근 가능
        # 'request' : 현재 요청 객체(APIView에서 전달된 request)로, 현재 요청을 보낸 사용자나 기타 요청 정보를 직렬화 클래스에서 참조하기 위해 사용
        serializer = PostSerializer(data=request.data, context={'request': request})  
        if serializer.is_valid(raise_exception=True):       # 유효성 검사 수행, 실패시 예외 발생
            serializer.save(user=request.user)      # # 현재 요청을 보낸 사용자를 user 필드에 설정 후 저장
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
        
    
class PostDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    # 주어진 post_id로 Post 객체를 가져오고, 없으면 404 오류 반환
    # 특정 post_id에 해당하는 Post 객체를 가져올때마다 호출된다. -> post_id가 유효하고 db에 해당 게시물이 있는지 확인하면서 Post 객체를 반환해주는 역할
    def get_object(self, post_id):
        return get_object_or_404(Post, pk=post_id)
    
    # 게시글 상세 조회
    def get(self, request, post_id):
        post = self.get_object(post_id)     # post_id에 해당하는 게시글 가져오기
        serializer = PostSerializer(post)       # Post 객체 직렬화
        return Response(serializer.data)        
    
    # 게시글 수정
    def put(self, request, post_id):
        post = self.get_object(post_id)     # post_id에 해당하는 게시글 가져오기
        
        # 현재 로그인한 사용자와 게시글 작성자가 다를 경우 오류 반환
        if post.user != request.user:
            return Response({'error' : '유효하지 않은 토큰입니다.'}, status=400)
        
        # 기존 post 객체에 새로운 데이터를 업데이트, 일부 필드만 업데이트 가능 (partial=True)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):       # 유효성 검사 수행, 실패시 예외 발생
            serializer.save()
            return Response(serializer.data)
        
    # 게시글 삭제
    def delete(self, request, post_id):
        post = self.get_object(post_id)     # post_id에 해당하는 게시글 가져오기
        if post.user != request.user:
            return Response({'error' : '유효하지 않은 토큰입니다.'}, status=400)
        post.delete()
        return Response(status=200)