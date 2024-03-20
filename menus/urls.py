from django.urls import path
import menus.views as views

urlpatterns = [
    path('updatecache', views.UpdateRedisCacheView.as_view()),
    path('get_omni_services', views.UpdateRedisOmniServicesView.as_view()),
]
