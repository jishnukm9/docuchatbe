
from django.urls import path,include
from .views import *
# from rest_framework_simplejwt.views import TokenVerifyView,TokenObtainPairView,TokenRefreshView,TokenBlacklistView

urlpatterns =[
    # path('api-auth/', include('rest_framework.urls')),
     path('login/',login,name='login'),
    #  path('logout/',logout_user,name='logout_api'),
   path('signup/',signup,name="signup"),
        path('testing/',testing,name="testing"),  
        path('logout/', logout, name='logout'),
        path('chatstream/', chat_stream, name='chatstream'),
        path('creativerse/', creati_verse, name='creativerse'),
]