from django.shortcuts import render
from accounts.models import User
from accounts.serializers import UserSerializer, ProfileUpdateSerialize, ChangePasswordSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model


class SignupAPIView(APIView):
    # 회원가입
    def post(self, request):
        # 요청 데이터로 UserSerializer 인스턴스 생성
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():   # 유효성 검사
            user = serializer.save()    # 유저 객체 저장
            if user:
                return Response(serializer.data, status=200)    # 저장된 유저 데이터 반환
        return Response(serializer.errors, status=400)      # 유효성 검사 실패시 오류 반환
            

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]      # 인증된 사용자만 접근 가능
    # 로그아웃
    def post(self, request):
        try:
            # refresh_token : 클라이언트가 요청 시 보내준 데이터에서 가져옴 
            # -> 클라이언트가 POST 요청으로 JSON 데이터를 서버에 보낼 때 해당 데이터 안에 refresh_token 키가 있어야 한다.
            refresh_token = request.data['refresh_token']       # 요청 데이터에서 refresh token 가져옴
            token = RefreshToken(refresh_token)     # refresh token 객체 생성 -> 토큰을 검증하고, 블랙리스트에 추가하여 더 이상 사용할 수 없도록 처리
            token.blacklist()       # 토큰을 블랙리스트에 추가해 로그아웃 처리
            return Response(status=200)
        except Exception:
            return Response({'error': '잘못된 요청입니다.'}, status=400)
        

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    # 프로필 조회
    def get(self, request, pk):
        # get_object_or_404 : 객체가 존재할 경우 해당 객체 반환, 없을 경우 404오류 반환
        # -> 특정 객체가 반드시 존재해야 하는 상황에서 사용
        # User : User 모델에서 데이터 조회 (accounts.models에서 가져온 것)
        user = get_object_or_404(User, pk=pk)       # pk에 해당하는 유저 객체 조회
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)


class ProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    # 프로필 수정
    def put(self, request, pk):
        user = get_object_or_404(get_user_model(), pk=pk)       # pk에 해당하는 유저 객체 조회

        if request.user.pk != user.pk:
            return Response({'error' : '권한이 없습니다.'}, status=400)     # 현재 로그인한 사용자와 pk가 다를 경우 권한 오류 반환
        
        # 업로드할 객체, 클라이언트로부터 전달된 데이터, 일부 필드만 업데이트 하도록 허용 (필드의 일부만 입력해도 유효성 검사 통과)
        serializer = ProfileUpdateSerialize(user, data=request.data, partial=True)      # 선택적 데이터 업데이트를 위해 partial=True 설정
        serializer.is_valid(raise_exception=True)       # 유효성 검사 실패 시 예외 발생
        serializer.save()       # 수정된 데이터 저장
        return Response(serializer.data)
    

class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]
    # 비밀번호 변경
    def put(self, request, pk):
        user = request.user     # 현재 로그인한 유저 객체
        serializer = ChangePasswordSerializer(user, data=request.data)      

        if serializer.is_valid():       # 유효성 검사
            serializer.save()
            return Response({'message' : '비밀번호가 변경되었습니다.'}, status=200)
        else:
            return Response(serializer.errors, status=400)
        

class UserDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]
    # 회원 탈퇴
    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)       # pk에 해당하는 유저 객체 조회
        password = request.data.get('password')     # 요청 데이터에서 비밀번호 가져옴
        if password is None:
            return Response({'error' : '비밀번호를 입력해주세요.'}, status=400)     # 비밀번호 미입력시 오류 반환
        
        if user.check_password(password):       # 비밀번호가 일치하는지 확인
            user.delete()       # 회원 탈퇴 처리
            return Response({'message' : '회원 탈퇴가 완료되었습니다.'}, status=200)
        return Response({'error' : '비밀번호가 일치하지 않습니다.'}, status=400)