from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from .models import CustomUser,PersonalToken,GroupToken,UserGroup,Users,GroupData,ChatData
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
# Create your views here.

# this is home page you can see all of your friend that joined in your chat
def Home(request,id,username):
    code = CustomUser.objects.get(username=username,is_active=True)
    hash_code = code.uuid
    return render(request,'app/home.html',{'id':id,'username':username,'hash_code':hash_code})


# this is chat page that people can send theire message together 
def Chat(request,id1,username1,id2,username2):
    try:
        person_a = PersonalToken.objects.get(sender=username1,receiver=username2)
    except PersonalToken.DoesNotExist:
        person_a=None
    try:
        person_b = PersonalToken.objects.get(sender=username2,receiver=username1)
    except PersonalToken.DoesNotExist:
        person_b=None
    
    if person_a is None and person_b is None:
        PersonalToken.objects.create(
            sender = username1,
            receiver = username2
        )
    return render(request,'app/chat.html',{'id1':id1,'username1':username1,'id2':id2,'username2':username2})


#this is general page that will remove in the future
def General(request):
    token = request.COOKIES.get('access_token')
    username = request.user
    user_id = request.user.id
    if not request.user.is_authenticated:
        return redirect('registration')
    if not token:
        return redirect('login')
    else:
        return redirect(f'/Home/{user_id}/{username}')

# this is for group page 
def Group(request,id,username):
    data = request.POST
    uuids = data.get('add_group')
    name = data.get('create_group')
    file = data.get('file')
    if name:
        GroupToken.objects.create(
            admin=username,
            groupname=name,
            picture = file
        )
    elif uuids:
        try:
            admin_name  = GroupToken.objects.get(group_uuid=uuids,admin=username)
        except GroupToken.DoesNotExist:
            admin_name=None
        try:
            is_avilabel = GroupToken.objects.get(group_uuid = uuids)
        except GroupToken.DoesNotExist:
            is_avilabel=None

        if admin_name is None and is_avilabel is not None:    
            group_name = is_avilabel.groupname
            g_uuid = is_avilabel.group_uuid
            picture = is_avilabel.picture
            try:
                UserGroup.objects.create(
                    admin = username,
                    groupname = group_name,
                    group_uuid = g_uuid,
                    picture = picture
                )
            except:
                return redirect(f'/Home/{id}/{username}/Group/')
    try:
        admin_data = GroupToken.objects.filter(admin=username)
    except GroupToken.DoesNotExist:
        admin_data = None
    
    try:
        user_data = UserGroup.objects.filter(admin=username)
    except UserGroup.DoesNotExist:
        user_data = None

    return render(request,'app/group.html',{'id':id,'username':username,'admin_data':admin_data,'user_data':user_data})

# this is Group chat page that people can chat in theire group 
def GroupChat(request,id,username,groupname):
    data = GroupToken.objects.get(groupname=groupname)
    avatar = data.picture
    return render(request,'app/group_chat.html',{'id':id,'username':username,'groupname':groupname,'avatar':avatar})

# this is profile page that save the information of person
def Profile(request,id,username):
    if request.method == 'POST':
        response = redirect('login')
        response.delete_cookie('access_token')
        return response
    else:
        data = CustomUser.objects.get(username=username)
        email = data.email
        first_name = data.first_name
        last_name = data.last_name
        phone = data.phone_number
        token = data.uuid
        password = data.password
        date_joind = data.date_joind
        return render(request,'app/Profile.html',{'id':id,'username':username,'email':email,'first_name':first_name,'last_name':last_name,'phone':phone,'token':token,'password':password,'date_joind':date_joind})

# this is logging page that people can login
def login_user(request):
    user = True
    if request.method == 'POST':
        data = request.POST
        email = data.get('email')
        password = data.get('password2')
        password1 = data.get('password1')
        if password != password1:
            return redirect('login')
        user = authenticate(email=email,password=password)
        if user is not None:
            login(request,user)
            username = user.username
            user_id = user.id
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            response = HttpResponseRedirect(f'/Home/{user_id}/{username}/')
            response.set_cookie('access_token',access_token,httponly=True,samesite='Lax',secure=True)
            response.set_cookie('refresh_token',str(refresh),httponly=True,samesite='Lax',secure=True)
            return response
    return render(request,'app/login.html',{'user':user})


# this is registration that people can register theire self in the chat system
def Registration(request):
    if request.method == 'POST':
        data = request.POST
        email = data['email']
        username = data['username']
        firstname = data.get('first')
        lastname = data.get('last')
        phone_number = data['number']
        password = data['password2']
        password1 = data.get('password1')
        if password != password1:
            return redirect('registration')
        CustomUser.objects.create(
            email=email,
            username=username,
            first_name = firstname,
            last_name = lastname,
            phone_number = phone_number,
            password=password
        )
        return redirect('login')
    return render(request,'app/registration.html')

# this is for change the password from profile
def Pasword(request,id,username):
    data = CustomUser.objects.get(username=username)
    email = data.email
    if request.method  == 'POST':
        password_data = request.POST
        password1 = password_data.get('pass1')
        password2 = password_data.get('pass2')
        if password1 != password2:
            return redirect(f'/Home/{id}/{username}/change_password/9mnjl/')
        else:
            data.set_password(password2)
            data.save()
            return redirect(f'/Home/{id}/{username}/Profile/a2b$/')
    return render(request,'app/Password.html',{'id':id,'username':username,'email':email})

# this is for change password from login
def forgot_Password(request):
    if request.method == 'POST':
        data = request.POST
        email = data.get('email')
        pass1 = data.get('pass1')
        pass2 = data.get('pass2')
        if pass1 != pass2:
            return redirect ('forgot')
        else:
            is_true = CustomUser.objects.get(email=email)

            if is_true is not None:
                is_true.set_password(pass2)
                is_true.save()
                return redirect('login')
    return render(request,'app/forgot.html')