'''
Serializer
데이터가 들어오면 JSON과 같이 특정한 포맷으로 변경해주는 것
serializer를 원하는 형태로 여러개를 만들어 놓고, 원할때 마다 바꿔가면서 사용할 수 있게 DRF 구조를 잡고 있다.
'''

from rest_framework import serializers
from .models import Article


# rest_framework에서 serializer를 가져오고, ModelSerializer를 상속받는다.
# Model을 통해 데이터를 주고받기 때문에 Model을 이용한 serializer가 정의되어 있다.
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        # Article Model에 있는 데이터를 가져와서 serializer 할거고, fields는 다 사용
        model = Article
        fields = '__all__'