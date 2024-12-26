from django.db import models
from django.conf import settings
import re
from django.core.exceptions import ValidationError

# Create your models here.
# 상품 이미지를 저장할 경로를 생성하는 함수
def product_image_path(instance, filename):
    return f'product_images/{instance.user.username}/{filename}' # 이미지 경로

# 파이썬의 정규표현식
# 해시태그가 유효한지 검사하는 사용자 정의 함수를 선언하자.(해시태그는 띄어쓰기와 특수문자가 허용되지 x)
def validation_hashtag(value):
    # 이 정규 표현식은 공백과 특수문자를 허용하지 않는 코드다.
    if not re.match(r'^[0-9a-zA-Z_]+$', value):
        raise ValidationError('해시태그는 알파벳, 숫자, 언더스코어만 가능합니다~!')
    
# 해시태그는 유일하며 중복되면 안 되기 때문에 따로 관리해야 한다. 또 각 게시물에도 중복된 해시태그를 설정할 수 없다.
# 하나의 해시태그는 여러 개의 물건과, 하나의 물건은 여러 개의 해시태그와 관계를 맺을 수 있다.

# 해시태그를 저장하는 모델
class HashTag(models.Model):
    name = models.CharField(max_length=50, unique=True, validators=[validation_hashtag])

    def __str__(self):
        return f'#{self.name}'
    
# 사용자의 등록한 상품을 저장하는 모델
class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')   # CASCADE : 사용자가 삭제되면 해당 사용자가 등록한 물품도 사라지게.
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to=product_image_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # 사용자가 상품에 '좋아요'를 누를 수 있음. 사용자와 좋아요와의 관계는 n:m, 즉 다대다 관계
    # ManyToManyField 로 다대다 관계 설정 가능(User 모델이랑.)
    # 상품에 좋아요가 없을 수도 있기 때문에 blank=True
    # 사용자가 좋아요를 누른 상품을 user.liked_products로 리스트로 참조 가능.
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_products', blank=True)
    # 상품과 연결되어 있는 해시태그(기본적으로 해시태그는 상품과 연결돼있다는 것.)
    # 다대다 관계
    hashtags = models.ManyToManyField(HashTag, related_name='products', blank=True)
    # 상품의 조회수
    views = models.PositiveIntegerField(default=0)  # 상품의 조회수는 음수가 될 수 없기에 PositiveIntegerField 사용

    def like_count(self):
        return self.likes.count()
    
    def __str__(self):
        return self.title