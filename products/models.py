from django import forms
from .models import Product, HashTag

class ProductForm(forms.ModelForm):
    hashtags_str = forms.CharField(required=False)  # 해시태그는 필수가 아니기 때문에 required=False.

    # 상품 폼을 생성할 때 중요한 것은 '사용자'! 즉, 누가 이 상품을 등록하는 가가 중요한 것이다.
    # 사용자를 뽑아서 해당 상품과 연결시켜주기 위함이다.
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)    # user 인자를 뽑는 것
        super().__init__(*args, **kwargs)   # 부모 클래스 초기화

    class Meta:
        model = Product
        fields = ['title', 'description', 'image', 'hashtags_str']

    # 로그인은 기본적으로 Django에서 save를 지원해줌. 그러나 상품 등록은 아니기 때문에 우리가 따로 만들어줘야 한다.
    # save 메서드는 폼에서 입력한 데이터를 db에 저장하는 것이다.
    def save(self, commit=True):    # commit=True : 바로 저장하겠다는 뜻.
        # 부모 클래스의 save 메서드를 호출하되, commit=False로 할 것이다 -> 해당 상품은 들고오되, db에는 해당 product를 저장하지 않겠다는 뜻. 왜? 해시태그와 상품을 함께 저장하기 위해.
        # 1. product 객체를 생성하고, 추가 작업(해시태그 처리)을 완료한 뒤에 commit을 한다(db에 반영한다.).
        # 2. user와 연결을 또 시켜줘야 함. 그 결과를 db에 적재하기 위해 일단 commit을 false로 둔다.
        product = super().save(commit=False)
        
        if self.user:
            product.user = self.user
        
        if commit:
            product.save()

        # 해시태그 처리
        # 입력받은 hashtag_str 문자열을 쉼표나 공백으로 구분해보자.(제한하는 것)
        # 각 해시태그를 db에 저장하거나, 이미 존재하면 가져올 것이다. 해시태그는 유일해야 하고 중복된 해시태그는 설정 불가 하니까!
        hashtags_input = self.cleaned_data.get('hashtags_str', '')
        hashtag_list = [h for h in hashtags_input.replace(',', ' ').split() if h]
        new_hashtags = []
        for ht in hashtag_list:
            ht_obj, created = HashTag.objects.get_or_create(name=ht)
            new_hashtags.append(ht_obj)

        # 다대다 관계 설정
        product.hashtags.set(new_hashtags)

        if not commit:
            product.save()

        return product