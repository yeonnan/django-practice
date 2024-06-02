from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Product


class ProductAPIView(APIView):
    # 인증되지 않은 유저는 get 읽기전용으로 제한
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        # 요청받은 데이터 title을 받아 title 변수에 넣는다.
        title = request.data.get('title')
        context = request.data.get('context')
        image = request.data.get('image')

        # title이나 context가 없으면 에러 발생
        if not (title and context):
            return Response({'error':'제목이나 내용을 작성해주세요.'})
        
        # 요청받아 들어온 데이터를 Product 모델에 저장. 
        product = Product.objects.create(
            user = request.user,
            title = title,
            context = context,
            image = image,
        )

        return Response({
            'pk':product.pk,
            'user':product.user.username,
            'title' : product.title,
            'context' : product.context,
            'image' : product.image.url,
        }, status=200)
    

    # 게시글 조회 
    def get(self, request):

        # Product 모델에 있는 모든 정보를 가져온다.
        products = Product.objects.all()
        # serializer를 사용하지 않고 json 형식으로 하려면 product 정보를 리스트 형식으로 반환
        # queryset은 여러 인스턴스의 집합 -> 개별 인스턴스에 접근하려면 반복문 사용필요
        product_list = []

        for product in products:
            product_data = {
            'pk': product.pk,
            'user': product.user.username,
            'title': product.title,
            'context' : product.context,
            'image' : product.image.url,
            }
            product_list.append(product_data)
        
        return Response(product_list, status=200)
    

class ProductDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        # get_object_or_404(모델 클래스, db에 저장된 게시글의 기본키) 
        # -> pk에 해당하는(게시글 id) Product 모델 반환, 해당 키를 가진 데이터가 없으면 404 반환
        product = get_object_or_404(Product, pk=pk)

        # 게시글을 작성한 유저와 로그인한 유저가 다르면 에러 반환
        if product.user != request.user:
            return Response({'error':'게시글 작성자가 아닙니다.'})
        
        # 요청받는 데이터 중 title에 해당하는 값을 가져옴, 
        # 변경하는 값이 없으면 product의 title. 즉, db에 저장되어 있는 title을 가져와서 사용
        title = request.data.get('title', product.title)
        context = request.data.get('context', product.context)
        image = request.data.get('image', product.image)

        # 게시글 수정 후 저장
        product.title = title
        product.context = context
        product.image = image 
        product.save()

        data = {
            'id':product.id,
            'title':product.title,
            'context':product.context,
            'image':product.image.url,
        }

        return Response(data, status=200)
    
    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        # 게시글을 작성한 유저와 로그인한 유저가 다르면 에러 반환
        if product.user != request.user:
            return Response({'error':'게시글 작성자가 아닙니다.'})
        
        product.delete()
        return Response({'게시글이 삭제되었습니다.'}, status=200)