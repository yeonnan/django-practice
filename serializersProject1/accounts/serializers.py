from rest_framework import serializers
from .models import User


# UserSerializer : ModelSerializer를 상속받아 사용자 모델 직렬화
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    # validated_data (검증된 데이터)를 사용하여 새로운 User 객체 생성
    def create(self, validated_data):
        # User 모델의 객체를 새롭게 생성
        # create_user : 비밀번호 해싱, 필수 필드 제공여부 확인, 유효한 데이터로 새로운 사용자 객체 생성 및 db에 저장
        user = User.objects.create_user(
            # validated_data : 클라이언트가 보낸 데이터가 유효하지 검사한 후 유효한 데이터만 저장
            # ['username'] : dict에서 username이라는 키에 해당하는 값을 가져옴
            # validated_data dict에서 username키에 해당하는 값을 가져와서 username 변수에 저장하는 것을 의미한다.
            username = validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            birthday=validated_data['birthday'],
            gender=validated_data['gender'],
            password=validated_data['password']
        )
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    # 쓰기 전용필드, 최소 8글자, required=True : 필수 항목
    password = serializers.CharField(write_only=True, min_length=8, required=True)

    class Meta:
        model = User
        fields = ['password']

    # 비밀번호 유효성 검사
    def validate_password(self, value):
        # 비밀번호가 8자 이하면 에러 발생
        if len(value) < 8:
            raise serializers.ValidationError("비밀번호는 8자 이상이어야 합니다.")
        # 유효성 검사를 통과한 값 반환
        # value : validate_password가 유효성 검사를 위해 메서드에 전달된 비밀번호
        return value

    # 사용자 인스턴스의 비밀번호를 업데이트
    def update(self, instance, validated_data):
        # instance : 수정하려는 기존 사용자 객체
        # validated_data : 유효성 검사를 통과한 데이터 -> 새 비밀번호
        # set_password : AbstractBaseUser에서 제공하는 메서드로 비밀번호를 해싱하고, 해싱된 비밀번호를 password 필드에 저장
        # 새 비밀번호를 해싱하여 인스턴스에 대입
        instance.set_password(validated_data['password'])
        # 변경된 비밀번호를 db에 저장
        instance.save()
        return instance