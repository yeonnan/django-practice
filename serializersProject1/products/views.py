from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from products.models import Product
from products.serializers import ProductSerializer
from rest_framework.response import Response


# 상품 등록, 목록 조회
class ProductView(APIView):
    # 상품 등록은 로그인 상태에서만 가능하지만, 상품 목록 조회는 로그인 상태 불필요
    # 사용자가 인증된 경우에만 쓰기 (post, put, delete)를 허용하고, 인증되지 않은 경우에는 읽기 (get)만 허용
    permission_classes = [IsAuthenticatedOrReadOnly]

    # 상품 목록 조회
    def get(self, request):
        # Product 모델에 있는 모든걸 가져온다.
        products = Product.objects.all()
        # serializer : 가져온 목록을 ProductSerializer로 직렬화 한다.
        # many=True 여러개의 객체를 직렬화할 때 사용한다. -> db에 저장되어 있는 모든 Product 객체를 직렬화해서 반환
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    # 상품 등록
    def post(self, request):
        # 요청으로 들어온 데이터를 가져온다.
        req_data = request.data 
        # 요청 데이터에 현재 사용자 id를 추가한다.
        # req_data['user'] : req_data의 dict에 'user' key를 추가 -> 직렬화 과정에서 user 필드로 사용
        # request.user.id : 현재 요청을 보낸 사용자의 id
        req_data['user'] = request.user.id
        # data=req_data : 클라이언트가 입력한 데이터를 포함한다.
        # serializer : 클라이언트가 입력한 데이터를 ProductSerializer로 직렬화한다.
        serializer = ProductSerializer(data=req_data)
        # 직렬화한 데이터가 유효하면 저장하고, 
        # raise_exception=True : 유효하지 않으면 예외를 발생시킨다.
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # 저장된 데이터를 응답으로 반환
            return Response(serializer.data,status=200)


class ProductDetailAPIView(APIView):
    # 인증된 사용자만 접근 가능
    permission_classes = [IsAuthenticated]

    # pk를 기준으로 Product 객체를 db에서 가져옴
    def get_object(self, pk):
        # 주어진 pk에 해당하는 Product 객체를 가져옴
        try:
            return Product.objects.get(pk=pk)
        # 객체가 존재하지 않으면 에러 문구와 함께 400 반환
        except Product.DoesNotExist:
            return Response({"error":"Product not found"}, status=400)

    # 상품 수정
    def put(self, request, pk):
        # get_object 메서드 호출 하면서 pk값을 전달하여 pk에 해당하는 Product 객체를 가져옴
        products = self.get_object(pk)

        # 토큰이 작성자의 토큰인지 확인
        # 작성자의 토큰이 아니라면 에러 문구와 함께 400 반환
        if products.user != request.user:
            return Response({"error":"유효하지 않은 토큰입니다."}, status=400)
        
        # 토큰이 유효하면 아래의 로직 실행
        # serializer : ProductSerializer에 괄호 안의 값 직렬화
        # products : pk에 해당하는 Product 객체, data는 요청받은 data, partial=True : 부분적 수정 허용
        serializer = ProductSerializer(products, data=request.data, partial=True)
        # 직렬화한 데이터가 유효하다면 저장하고, 직렬화한 데이터 반환
        # raise_exception=True : 유효하지 않으면 예외를 발생시킨다.
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    # 상품 삭제
    def delete(self, request, pk):
        # get_object 메서드 호출 하면서 pk값을 전달하여 pk에 해당하는 Product 객체를 가져옴
        products = self.get_object(pk)
        # 토큰이 작성자의 토큰인지 확인, 작성자의 토큰이 아니라면 에러 문구와 함께 400 반환
        if products.user != request.user:
            return Response({"error":"유효하지 않은 토큰입니다."}, status=400)
        
        products.delete()
        return Response(status=200)