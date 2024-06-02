from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date


class User(AbstractUser):
    # 내부 클래스로 정의하면 코드가 더 명확하고 읽기 쉬우며, 코드의 재사용성이 좋다.
    class GenderChoices(models.TextChoices):
        # 'M' : db에 저장될 실제 값, '남성' : 사람이 읽을 값으로 인터페이스에 표시
        Male = 'M','남성'
        Female = 'F', '여성'

    birthday = models.DateField(
        # validators : 모델 필드에서 유효성 검사할 떄 사용
        validators=[
            MinValueValidator(date(1900, 1, 1)),    # 1900.1.1 이전의 생일 허용하지 않음
            MaxValueValidator(date.today())     # 미래 날짜 입력 불가
        ]
    )

    # 첫번째 choices : CharField의 인자. 필드의 값으로 혀용되는 선택지를 지정한다.
    # 두번째 choices : models.TextChoices 클래스의 속성 (value, display_name) 형식의 튜플 리스트 반환
    # GenderChoices : [('M', '남성'), ('F', '여성')] 튜플 리스트 반환
    gender = models.CharField(max_length=1, choices=GenderChoices.choices)

    introduction = models.TextField(default="")

    # REQUIRED_FIELDS : 사용자 생성시 필수로 입력되어야 하는 필드 목록 지정
    # AbstractUser는 username, email, password를 필수로 요구한다.
    REQUIRED_FIELDS = ['birthday']