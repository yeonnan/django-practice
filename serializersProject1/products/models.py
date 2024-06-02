from django.db import models
from django.conf import settings

class Product(models.Model):
    # settings의 AUTH_USER_MODEL 사용
    # AUTH_USER_MODEL = 'accounts.User' -> model이 바뀌어도 settings만 변경해서 사용할 수 있게
    # on_delete=models.CASCADE : 참조된 객체가 삭제될 때, 해당 외래키가 참조하고 있는 모든 객체도 같이 삭제된다.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # CharField : 최대 길이 제한이 있다.
    title = models.CharField(max_length=120)
    # TextField : 길이에 제한이 없는 긴 텍스트 저장 가능
    context = models.TextField()
    # blank = True : django의 폼에서 해당 필드가 비어 있는 상태로 허용, 폼 제출 시 해당 필드가 비어 있어도 유효성 검사를 통과
    # null = True : db에서 해당 필드가 null값을 가질 수 있도록 허용, 즉 필드에 아무런 값도 저장되지 않은 상태를 의미
    image = models.ImageField(blank=True, null=True)
