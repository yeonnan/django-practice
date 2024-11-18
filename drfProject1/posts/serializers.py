from rest_framework import serializers
from .models import Post
from django.contrib.auth import get_user_model

# 현재 프로젝트에서 사용 중인 사용자 모델을 가져옴
User = get_user_model()     

class PostSerializer(serializers.ModelSerializer):
    category = serializers.ChoiceField(choices=Post.Category.choices)

    class Meta:
        model = Post
        fields = '__all__'
        # 해당 필드를 읽기 전용으로 설정하여 클라이언트에서 수정하지 못함
        read_only_fields = ['user', 'user_nickname', 'created_at', 'updated_at']

    def create(self, validated_data):
        # 현재 요청을 보낸 사용자를 작성자로 설정 (user 필드에 추가)
        validated_data['user'] = self.context['request'].user   
        # 부모 클래스의 create 메서드를 호출하여 Post 객체를 생성하고 반환
        # super : 부모 클래스를 호출하는 python 문법. 여기서는 ModelSerializer
        # PostSerializer는 ModelSerializer를 상속받았기 때문에 ModelSerializer에 정의된 create 메서드를 super().create()로 호출가능
        return super().create(validated_data)       # 부모 클래스인 ModelSerializer의 create 메서드를 호출하여, 유효성 검사를 통과한 데이터(validated_data)로 새로운 Post 객체를 생성하고 데이터베이스에 저장



'''
validated_data['user'] = self.context['request'].user 

validated_data['user'] : user는 Post 모델의 user 필드에 값을 할당, 
validated_data 딕셔너리의 user 키에 값을 추가하거나 기존 값을 수정하는 방식으로 현재 요청을 보낸 사용자를 user 필드에 설정하는 역할
context : serializer 인스턴스에 전달된 추가적인 데이터가 담긴 속성, APIView에서 serializer를 생성할 때 context를 통해 추가 정보를 전달
self.context['request'] : context에 전달된 request 객체를 의미

-> 현재 요청을 보낸 사용자를 validated_data의 user 필드에 할당하여, Post 객체 생성 시 user 필드에 자동으로 설정
'''


'''
ModelSerializer
모델 인스턴스를 JSON과 같은 형식으로 자동 변환해주고, 
클라이언트로 부터 받은 데이터를 모델 인스턴스로 변환하여 저장할 수 있도록 돕는 직렬화 도구
'''