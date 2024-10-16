from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import Home,login_user,General,Registration,Chat,Group,GroupChat,Profile,Pasword,forgot_Password

urlpatterns = [
    path('',General,name='general'),
    path('Home/<int:id>/<str:username>/',Home,name='home'),
    path('login/',login_user,name='login'),
    path('registration/',Registration,name='registration'),
    path('Home/<int:id1>/<str:username1>/chat/<int:id2>/<str:username2>/',Chat,name='chat'),
    path('Home/<int:id>/<str:username>/Group/',Group,name='Group'),
    path('Home/<int:id>/<str:username>/<str:groupname>/',GroupChat,name='GroupChat'),
    path('Home/<int:id>/<str:username>/Profile/a2b$/',Profile,name='profile'),
    path('Home/<int:id>/<str:username>/change_password/9mnjl/',Pasword,name='Password'),
    path('forgot_password/',forgot_Password,name='forgot'),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)