
from django.urls import path
from chatapp import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    # path('login/',views.login,name='login'),
    path('',views.home,name='home'),
    # path('logout/',views.logout_view,name='logoutuser'),
    # path('register/',views.registration_view,name='registeruser'),
    path('app/<app>/',views.app,name='app'),

]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)