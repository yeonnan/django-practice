from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # unique = True : 고유한 값
    nickname = models.CharField(max_length=20, unique=True)
    # null=True : 데이터베이스에서 NULL 값을 허용, 해당 필드에 데이터가 없으면 데이터베이스에 NULL 값으로 저장
    # blank=True : 폼 유효성 검사에서 빈 값을 허용, 입력 폼에서 필수 입력이 아님
    # null=False, blank=True : 폼에서는 비울 수 있지만, 데이터베이스에 저장할 때는 반드시 값이 필요하다.
    image = models.ImageField(upload_to='media/accounts/', null=True, blank=True)
    # 유저 생성 시 자동으로 생성되는 필드, 생성된 날짜와 시간 저장
    created_at = models.DateTimeField(auto_now_add=True)
    # 유저 정보가 수정될 때마다 자동으로 업데이트돠는 필드, 수정된 날짜와 시간 저장
    updated_at = models.DateTimeField(auto_now=True)
    age = models.CharField(max_length=3)

    # 유저 생성 시 필수로 입력해야 하는 필드 목록 지정
    # AbstractUser의 기본 필드와 함께 nickname, age 필드
    # AbstractUser 기본 필드 : username, password, email, first_name, last_name, is_staff, is_active, date_joined
    REQUIRED_FIELDS = ['nickname', 'age']


'''
username: 유저 이름을 나타내는 고유 필드로, 기본적으로 필수 입력 사항입니다.
password: 유저의 비밀번호를 저장하는 필드.
email: 이메일 주소를 저장하는 필드.
first_name: 유저의 이름(First name).
last_name: 유저의 성(Last name).
is_staff: 유저가 관리자 권한을 가졌는지 여부를 나타내는 Boolean 필드.
is_active: 유저가 활성화되어 있는지를 나타내는 Boolean 필드.
date_joined: 유저가 계정을 생성한 날짜와 시간을 나타내는 필드.
'''