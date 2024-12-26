from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
def user_profile_image_path(instance, filename):
    return f'profile_images/{instance.username}/{filename}' # 이미지 경로

# 프로필 이미지, 팔로우 수, 팔로잉 수를 추가적으로 선언해야 한다.
class User(AbstractUser):
    profile_image = models.ImageField(upload_to=user_profile_image_path, blank=True, null=True)    # image가 어디에 있는 지. 이미지를 입력하면 instance와 filename을 받는다.

    # 팔로우
    follows = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)   # 자기 자신은 팔로우하지 못하니까 symmetricla을 False로 한 것. related_name은 어떤 테이블을 참고할 지.

    @property   # static한 함수. 절대 바뀌지 않는 함수. 즉, 이 함수는 정적인 파일의 함수다 라고 선언한 것.
    # 팔로워
    def follower_count(self):
        return self.followers.count()
    
    @property
    # 팔로윙
    def following_count(self):
        return self.follows.count()
    
    def __str__(self):
        return self.username