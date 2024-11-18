from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    # User 모델 필드를 포함하는 직렬화 클래스
    # class Meta : 직렬화할 모델과 필드를 지정하는데 사용
    class Meta:
        model = User    # 직렬화할 모델 지정
        fields = '__all__'

    def create(self, validated_data):
        # 사용자 생성 시 create_user 메서드를 사용하여 비밀번호가 해시 처리되도록 함
        # create_user : AbstractBaseUser를 상속한 모델에서 제공하는 내장 함수
        user = User.objects.create_user(
            # validated_data['field_name']: 해당 필드가 반드시 존재해야 한다. 만약 field_name 키가 validated_data에 없을 경우 KeyError 발생
            # validated_data.get('field_name') : 해당 필드를 가져온다. 필드가 존재하지 않으면 None을 반환하므로 KeyError가 발생하지 않는다.
            username = validated_data['username'],      
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'],
            password = validated_data['password'],      # 비밀번호 해시 처리되어 저장
            nickname = validated_data['nickname'],
            age = validated_data['age'],
            image = validated_data.get('image')     # 이미지가 선택적 필드일 수 있으므로 get 메서드 사용
        )
        return user
    

class ProfileUpdateSerialize(serializers.ModelSerializer):
    # 사용자 프로필 업데이트를 위한 직렬화 클래스
    class Meta:
        model = User
        fields = ['nickname', 'email']      # 닉네임과 이메일만 업데이트 가능하도록 설정

    # 이메일 중복 확인을 위해 현재 인스턴스를 제외한 동일 이메일 존재 여부 확인
    def validate_email(self, value):
        # user에 현재 인스턴스 할당
        user = self.instance
        # User 모델의 객체들 중 현재 인스턴스를 제외하고 동일한 이메일이 존재하는지 확인
        # exclude : 특정 조건에 해당하는 객체를 제외하고 나머지 객체 반환, 현재 수정 중인 사용자(self.instance)를 중복 검사에서 제외하기 위해 사용
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            # 중복된 이메일이 존재하면 ValidationError 발생
            raise serializers.ValidationError({"email": "사용중인 이메일 입니다."})
        # 이메일이 중복되지 않는 경우 입력된 이메일 값 그대로 반환
        return value
    
    # 닉네임 중복 확인을 위해 현재 인스턴스를 제외한 동일 닉네임 존재 여부 확인
    def validate_nickname(self, value):
        user = self.instance
        # exclude(pk=user.pk): 현재 사용자 객체를 제외
        # filter(nickname=value): 다른 사용자 중 닉네임이 value와 같은 객체를 필터링
        # exists(): 동일한 닉네임을 가진 사용자가 존재하면 True를 반환
        if User.objects.exclude(pk=user.pk).filter(nickname=value).exists():
            raise serializers.ValidationError({"nickname": "사용중인 닉네임 입니다."})
        return value
    
    # 인스턴스의 이메일과 닉네임 업데이트
    def update(self, instance, validated_data):
        # validated_data에서 'email'을 가져와 인스턴스의 email 필드에 할당
        # validated_data에 email이 없다면, 기존 instance.email 값 유지
        # validated_data.get('email', instance.email) : validated_data dict에서 email 키를 가져온다.
        instance.email = validated_data.get('email', instance.email)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        # 변경된 내용을 DB에 저장
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    # 비밀번호 변경을 위한 직렬화 클래스
    class Meta:
        model = User
        fields = ['password']
    
    def validate_password(self, value):
        # 비밀번호 최소 길이 검증 (8글자 이상)
        if len(value) < 8:
            raise serializers.ValidationError('비밀번호는 8글자 이상이어야 합니다.')
        return value
    
    def update(self, instance, validated_data):
        # 새 비밀번호 설정 시 set_password 메서드를 사용하여 비밀번호 해시 처리
        instance.set_password(validated_data['password'])
        instance.save()
        return instance