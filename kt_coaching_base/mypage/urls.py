from django.urls import path
from . import views
from rpg import views as rpg_views
app_name = 'mypage'

urlpatterns = [
    path('', views.mypage_view, name='mypage_view'),
    path('mypage_info/', views.box_info, name='box_info'),
    path('mypage_self/', views.box_self, name='box_self'),
    # path('mypersona/', rpg_views.mypersona, name='mypersona'),
]
