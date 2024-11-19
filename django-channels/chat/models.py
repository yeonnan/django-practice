from django.conf import settings
from django.db import models


class RolePlayingRoom(models.Model):
    class Language(models.TextChoices):
        ENGLISH = 'en-US', 'English'
        SPANISH = 'es=ES', 'Spanish'
        FRENCH = "fr-FR", "French"
        GERMAN = "de-DE", "German"
        RUSSIAN = "ru-RU", "Russian"
        JAPANESE = "ja-JP", "Japanese"
        CHINESE = "zh-CN", "Chinese"


    class Level(models.IntegerChoices):
        BEGINNER = 1, '초급'
        ADVANVED = 2, '고급'


    # 모델로부터 파생되는 queryset에 디폴트 정렬 방향 지정 -> 디폴트 정렬 방향 : 기본 키에 대한 역순 정렬
    class Meta:
        ordering = ['-pk']


    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    language = models.CharField(max_length=10, choices=Language.choices, default=Language.ENGLISH, verbose_name='대화 언어')
    level = models.SmallIntegerField(choices=Level.choices, default=Level.BEGINNER, verbose_name='레벨')
    situation = models.CharField(max_length=100, verbose_name='상황')
    situation_en = models.CharField(
                                    max_length=100, 
                                    blank=True, 
                                    verbose_name='상황 (영문)',
                                    help_text='GPT 프롬프트에 직접적으로 활용됩니다. 비워두시면 situation 필드를 번역하여 자동 반영됩니다.'
                                    )
    my_role = models.CharField(max_length=100, verbose_name='내역할')
    my_role_en = models.CharField(
                                max_length=100, 
                                blank=True, 
                                verbose_name='내역할 (영문)',
                                help_text='GPT 프롬프트에 직접적으로 활용됩니다. 비워두시면 my_role 필드를 번역하여 자동 반영됩니다.'
                                )
    gpt_role = models.CharField(max_length=100, verbose_name='GPT 역할')
    gpt_role_en = models.CharField(
                                max_length=100, 
                                blank=True, 
                                verbose_name='GPT 역할 (영문)',
                                help_text='GPT 프롬프트에 직접적으로 활용됩니다. 비워두시면 gpt_role 필드를 번역하여 자동 반영됩니다.'
                                )
    
