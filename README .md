# 🤖 RAG를 활용한 Sparta 복습용 챗봇 만들기

## 📖 목차
1. [How To Use](#-how-to-use)
2. [Directory Structure](#-directory-structure)
3. [팀 소개 및 협업 도구](#-팀-소개-및-협업-도구)
4. [프로젝트 소개](#-프로젝트-소개)
5. [프로젝트 계기](#-프로젝트-계기)
6. [프로젝트 핵심 목표](#-프로젝트-핵심-목표)
7. [Key Summary](#️-key-summary)
8. [인프라 아키텍처 & 적용 기술](#-인프라-아키텍처-적용-기술)
9. [주요기능](#-주요기능)
10. [서비스 구조](#-서비스-구조)
11. [기술적 고도화](#-기술적-고도화)
12. [Timeline](#-timeline)

---
## 📣 How To Use
1. 원격 저장소에 올라와 있는 코드 clone 받기
```python
git clone https://github.com/ysooj/CH4-DRF.git
```

2. 가상환경 생성 및 활성화
    - 가상환경 생성
    ```python
    python -m venv 가상환경이름
    ```
    - 가상환경 활성화
    ```python
    # MacOS
    source 가상환경이름/bin/activate
    # Windows
    source 가상환경이름/Scripts/activate
    ```

3. requirements.txt 설치
```python
pip freeze > requirements.txt
```

4. 서버 실행 
```python
python manage.py runserver
```

5. 웹 페이지 실행
터미널 창의 주소를 Ctrl + 클릭 해서 웹 페이지에 접속할 수 있습니다.
```
http://127.0.0.1:8000/
```
   
---
## 🔍 Directory Structure

```
clone한 폴더/
├── accounts/
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── templates/accounts
│   │   ├── login.html
│   │   ├── profile.html
│   │   ├── profile_edit.html
│   │   └── signup.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── media/
├── products/
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── templates/products
│   │   ├── product_detail.html
│   │   ├── product_form.html
│   │   └── product_list.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── spartamarket/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/images
├── .gitignore
├── ERD.drawio
└── manage.py
```

---
## 📋 프로젝트 소개
- 프로젝트명 : spartamarket
- 개발 기간 : 2024.12.19 - 2024.12.27

---
## ❕ 프로젝트 핵심 목표
Django를 사용하여 웹 애플리케이션의 기본 기능을 설계하고 구현하는 방법을 익힙니다. 효율적인 데이터 관리를 위해 ERD를 작성하고 데이터베이스 모델을 설계하는 법을 배웁니다. 또한, 프로젝트의 목적과 구조, 설치 방법 등을 명확히 전달할 수 있도록 README 파일을 작성하는 연습을 합니다.

---
## 🗝️ Key Summar
- accounts 앱과 products 앱으로 나눠서 각각 user 관련, product 관련 기능으로 나눴습니다.
- accounts 앱에서 회원가입, 로그인, 로그아웃, 프로필, 팔로우 기능을 구현했습니다.
- products 앱에서 상품 등록, 상품 목록 조회, 상품 상세 조회, 상품 상세 수정, 상품 상세 삭제, 찜하기 기능을 구현했습니다.
- 개별 프로필 사진, 해시태그 기능 등 도전 기능도 구현했습니다.
      
- 주요 트러블 슈팅 사례
   <details>
  <summary>오타 문제</summary>
    변수나 함수명, html 등의 오타로 인해 다양한 오류가 발생해서, 오타를 찾아서 수정하는 작업이 많았습니다.
  </details>

  </details>

  <details>
  <summary>html로 연결할 수 없다는 에러</summary>
   원인 : pk값을 인자로 넘겨주지 않았습니다.
   
   문제 코드
   ```
    <h3>내가 등록한 물품들</h3>
    <ul>
    {% for product in my_products %}
        <li><a href="{% url 'products:product_detail' %}">{{ product.title }}</a></li>
    {% empty %}
        <li>등록한 물품이 없습니다.</li>
    {% endfor %}
    </ul>
   ```
   
   해결 코드
   ```
    <h3>내가 등록한 물품들</h3>
    <ul>
    {% for product in my_products %}
        <li><a href="{% url 'products:product_detail' product.pk %}">{{ product.title }}</a></li>
    {% empty %}
        <li>등록한 물품이 없습니다.</li>
    {% endfor %}
    </ul>
   ```
  </details>

---
## ✅ 웹 페이지 
- 회원가입
<p align="center">
    <img width="1582" alt="회원가입" src="https://github.com/user-attachments/assets/17eaf7cf-f7cb-43df-931b-e19f0d0b62fb" />
</p>
- 로그인
<p align="center">
    <img width="1582" alt="로그인" src="https://github.com/user-attachments/assets/2fedf9aa-8b25-4d2f-a66f-60a34f53525c" />
</p>
- 상품 목록
<p align="center">
    <img width="1582" alt="상품 목록" src="https://github.com/user-attachments/assets/4bbfcbcb-39f9-4418-8ed1-b6f42ded8ea8" />
</p>
- 상품 상세
<p align="center">
    <img width="1582" alt="상품 상세" src="https://github.com/user-attachments/assets/4200970b-aa5f-4b0c-81a6-3d6a4f115436" />
</p>
- 상품 등록
<p align="center">
    <img width="1582" alt="상품 등록" src="https://github.com/user-attachments/assets/4dd77ea1-08f9-44cd-9cea-ebb0ab4bcb9b" />
</p>
- 프로필
<p align="center">
    <img width="1582" alt="프로필" src="https://github.com/user-attachments/assets/ed755087-bf3e-4a4c-9a8e-a4125c11bae9" />
</p>
- 프로필 수정
<p align="center">
    <img width="1582" alt="프로필 수정" src="https://github.com/user-attachments/assets/d514b6c4-b376-4f2c-aab7-e1ce6dc21031" />

</p>
