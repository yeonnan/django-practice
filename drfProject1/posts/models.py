from django.db import models
from django.conf import settings


class Post(models.Model):
    class Category(models.TextChoices):
        FREE_BOARD = 'FREE BOARD', '자유 게시판'        # FREE BOARD : DB에 저장되는 값, 자유 게시판 : 사용자에게 보여지는 값
        INFO_BOARD = 'INFO BOARD', '정보 공유'      # INFO BOARD : DB에 저장되는 값, 정보 공유 : 사용자에게 보여지는 값
    
    # FK로 Post 모델과 사용자 모델 연결, 해당 게시물을 작성한 사용자 지정
    # settings.AUTH_USER_MODEL을 사용해 사용자 모델 참조
    # on_delete=models.CASCADE : 사용자 삭제 시 연결된 게시물도 함께 삭제
    # related_name='posts' : User 모델에서 해당 사용자가 작성한 게시물을 참조할 수 있는 역참조 이름
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    user_nickname = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=10, choices=Category.choices)


'''
related_name
ForeignKey나 ManyToManyField와 같은 관계 필드에서 역참조 이름을 지정하기 위해 사용
'''