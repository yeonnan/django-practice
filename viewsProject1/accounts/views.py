from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated


class UserAPIView(APIView):
    def post(self, request):
        # 요청한 데이터를 가져옴
        data = request.data
        # username과 email은 존재해야 하며, 중복이 있으면 안되므로 username과 email의 유효성 검사를 위해
        # 데이터를 먼저 가져온다.
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # username과 email 둘 중 하나라도 없으면 로그인 불가능
        if not (username and email and password):
            return Response({'error':'username 또는 email, password가 필요합니다.'}, status=400)
        
        # username과 email 중복 시 에러 반환
        # 선언한 User 모델을 가져옴 - db에 있는 email과 요청한 데이터 email이 같은지 확인
        # exists - 데이터베이스 조회 결과가 존재한다면 True를 반환, 없으면 False를 반환한다.
        # db에 있는 모델이 같다 - True - 에러 반환
        if get_user_model().objects.filter(username=username).exists():
            return Response({'error':'동일한 username이 있습니다.'}, status=400)
        
        if get_user_model().objects.filter(email=email).exists():
            return Response({'error':'동일한 email 있습니다.'}, status=400)

        # 데이터 반환
        # 코드를 읽는 사람이 create_user가 무엇인지 이해하기 쉽도록 하며,
        # 생성된 정보를 직접 추출하여 민감한 정보를 제외하고 서버로 반환 가능
        # create_user : User 모델의 username, email, password 등을 저장하고 반환한다.
        # 왼쪽 : 데이터를 가지고 생성된 사용자 객체 / 오른쪽 : 요청 받은 데이터 (request.data)
        user = get_user_model().objects.create_user(
            username = username,
            email = email,
            password = password,
            gender = data.get('gender'),
            first_name = data.get('first_name'),
            last_name = data.get('last_name'),
            birthday = data.get('birthday'),
        )

        # id, username, email 반환
        # 왜 3개만 반환하는가? 다른 정보는 민감한 개인정보. 원한다면 다른 데이터도 반환 가능하다.
        # user객체의 id, username, email
        return Response({
            'id' : user.id,
            'username' : user.username,
            'email' : user.email,
        }, status=200)
    

class UserDetailAPIView(APIView): 
    # 로그인한 사용자만 접근 가능
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        # user 객체가 데이터 요청을 받는다. 
        # 이때 현재 로그인한 사용자의 정보를 받는다.
        user = request.user

        # url로 받은 username이 로그인한 사용자의 username과 다르다면 에러 발생
        if username != user.username:
            return Response({'error':'사용자 계정이 일치하지 않습니다.'})
        
        # 사용자의 정보와 일치하다면 반환
        return Response({
            'id' : user.id,
            'username' : user.username,
            'email' : user.email,
            'gender' : user.gender,
            'first_name' : user.first_name,
            'last_name' : user.last_name,
            'birthday' : user.birthday,
        }, status=200)