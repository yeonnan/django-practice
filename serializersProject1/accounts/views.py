from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.serializers import UserSerializer, ChangePasswordSerializer
from django.shortcuts import get_object_or_404
from accounts.models import User
from django.contrib.auth import logout, get_user_model
from rest_framework.permissions import IsAuthenticated

# 회원가입, 로그인, 로그아웃, 프로필페이지, 본인정보 수정, 회원탈퇴, 비밀번호 변경


# 회원가입
class SignupAPIView(APIView):
    def post(self, request):
        # serializer : 요청받은 데이터를 가져와 UserSerializer에 데이터를 입력한다.
        serializer = UserSerializer(data=request.data)
        # 입력받은 데이터가 유효하다면 user 객체에 데이터 저장되며 201 return
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=201)
        # 입력받은 데이터가 유효하지 않다면 serializer 에러를 반환하며 400 return
        # serializer.errors : 직렬화된 데이터가 유효하지 않으면 발생하는 에러
        return Response(serializer.errors, status=400) 
    
    # 회원 탈퇴
    def delete(self, request):
        # 현재 로그인한 사용자
        user = request.user
        # 요청 데이터에서 비밀번호 추출
        password = request.data['password']
        # 비밀번호가 일치한다면 삭제
        if user.check_password(password):
            user.delete()
            return Response({'message':'반가웠습니다.'}, status=200)
        return Response({'error':'비밀번호가 맞지 않습니다.'}, status=400)


# 로그아웃
class LogoutAPIView(APIView):
    # 인증된 사용자만 접근 가능
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # logout : django의 내장함수, 사용자의 세션을 무효화하고, 로그인 상태 해제
        # 현재 요청과 연관된 세션 데이터를 제거하여 로그아웃
        logout(request)
        return Response({'message':'로그아웃 되었습니다.'}, status=200)


class UserDetailAPIView(APIView):
    # 인증된 사용자만 접근 가능
    permission_classes = [IsAuthenticated]

    # 프로필 조회
    def get(self, request, username):
        # get_object_or_404 : User 모델에서 username에 해당하는 객체를 가져오는데, 없으면 404를 반환한다.
        # 왼쪽 username : User 모델에 정의된 username, 오른쪽 username : get에서 전달받은 username
        # 즉, User 모델의 username이 전달받은 username과 일치하는 객체를 조회하라는 의미
        user = get_object_or_404(User, username=username)
        # user객체를 UserSerializer를 사용하여 직렬화하는 과정
        # User 모델을 직렬화하여 json 형식으로 변환
        serializer = UserSerializer(user)
        # serializer.date : 직렬화된 데이터를 의미 -> 파이썬의 dict 형태로 변환된 데이터
        return Response(serializer.data)

    # 본인 정보 수정
    def put(self, request, username):
        # get_user_model : 현재 활성화된 사용자 모델 반환
        # 현재 활성화된 사용자 모델의 username이 전달받은 username과 일치하는 객체를 조회하고 없으면 404 반환
        user = get_object_or_404(get_user_model(), username=username)

        # 요청한 사용자가 조회된 user 객체와 일치하지 않으면 403 반환
        # 뒤에온 user : get_object_or_404에 의해 조회된 사용자 객체
        if request.user != user:
            return Response({'error':'permission denied'}, status=403)
        
        # 요청받은 데이터를 user 객체를 사용하여 UserSerializer로 직렬화
        # partial=True : 부분 업데이트를 허용 (모든 필드가 필요하지 않음)
        serializer = UserSerializer(user, data=request.data, partial=True)

        # 요청받은 값이 유효하면 저장하며, 값이 틀리면 예외 반환
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 업데이트된 데이터 반환
        return Response(serializer.data)
    

# 비밀번호 변경
class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        # 현재 로그인한 사용자
        print('우재님은귀엽따')
        user = request.user
        print(user)
        # 사용자로부터 받은 데이터와 현재 사용자를 바탕으로 serializer 생성
        serializer = ChangePasswordSerializer(user, data=request.data)

        # 데이터 유효성 검사
        # 직렬화한 데이터가 유효하다면 -> db에 값이 저장되며 200 반환
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'비밀번호가 변경되었습니다.'}, status=200)
        # 데이터가 유효하지 않다면 오류 반환
        else:
            return Response(serializer.errors, status=400) 
