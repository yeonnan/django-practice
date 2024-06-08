from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
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
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    # 상품 등록
    def post(self, request):
        pass
