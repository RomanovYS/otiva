from django.urls import path
import main_app.views as main_app

app_name = 'main_app'

urlpatterns = [
    path('', main_app.MainPageView.as_view(), name='main_page'),
    path('cabinet/', main_app.UserCabinetView.as_view(), name='cabinet'),
    path('my_advert/', main_app.UserGoodsView.as_view(), name='my_advert'),
    path('add_good/', main_app.AddGoodView.as_view(), name='add_good'),
    path('add_device/', main_app.AddDeviceView.as_view(), name='add_device'),
    path('detail/<int:pk>/', main_app.GoodDetailView.as_view(), name='good_detail'),
]
