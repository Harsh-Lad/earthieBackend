from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import User, HomeSlider, HomeBlock, Categories, Products, Collections
from uuid import uuid4
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .serializers import HomeSliderSerializer, HomeBlockSerializer, CategorySerializer, ProductSerializer, CollectionsSerializer
from django.db.models import Q

# Create your views here.

# customizing token claims
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['name'] = user.first_name
        token['email'] = user.email
        return token
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(('GET',))
def home(req):
    return Response('It works',status=status.HTTP_200_OK)

@api_view(('GET','POST'))
def signupView(req):
    if req.method == 'POST':
        data = req.data
        name = data['name']
        email = data['email']
        phone = data['phone']
        password = data['password']
        user = User.objects.filter(email=email)
        if user:
            return Response('User Already Exists! Please Login',status=status.HTTP_200_OK)
        else:
            token = name+str(uuid4())+str(phone)
            user = User.objects.create(first_name=name,email=email,phone=phone,token=token)
            user.set_password(password)
            user.save()
            name = name.capitalize()
            link = f"http://127.0.0.1:8000/verify?token={token}"
            msg_plain = render_to_string('activation.txt', {'name': name ,'verificationLink':link})
            msg_html = render_to_string('activation.html', {'name': name,'verificationLink':link})

            send_mail(
                "Verify your Email",
                msg_plain,
                "earthie@mggroupindia.in",
                [email],
                 html_message=msg_html,
                fail_silently=False,
            )
            return Response('Registered Successfully! Please login',status=status.HTTP_200_OK)
    return Response('Method not allowed',status=status.HTTP_200_OK)
    
@api_view(('GET',))
def verify(req):
    token = req.GET.get('token',None)
    if token:
        try:
            user = User.objects.get(token=str(token))
            user.is_verified = True
            user.save()
            name = user.first_name.capitalize()
            email = user.email
            msg_plain = render_to_string('activationDone.txt', {'name': name})
            msg_html = render_to_string('activationDone.html', {'name': name})
            send_mail(
                "Congratulations",
                msg_plain,
                "earthie@mggroupindia.in",
                [email],
                    html_message=msg_html,
                fail_silently=False,
            )
            return Response('Congratulations! Email verified successfully',status=status.HTTP_200_OK)
        except:
            return Response('Invalid Url',status=status.HTTP_200_OK)
    return Response('Invalid Url',status=status.HTTP_200_OK)

@api_view(('GET',))
def homeSlider(req):
    slider = HomeSlider.objects.all()
    serializer = HomeSliderSerializer(slider,many=True).data
    return Response(data=serializer, status=status.HTTP_200_OK)

@api_view(('GET',))
def homeBlock(req):
    slides = HomeBlock.objects.all()
    serializer = HomeBlockSerializer(slides, many=True).data
    return Response(data=serializer, status=status.HTTP_200_OK)

@api_view(('POST',))
def forgotpasswordEmail(req):
    if req.method == 'POST':
        reqData = req.POST['email']
        try:
            user = User.objects.get(email=reqData)
            token = user.first_name+str(uuid4())+str(user.phone)+"forgot-password"
            user.token = token
            user.save()
            link = f"http://127.0.0.1:8000/setPassword?token={token}"
            msg_plain = render_to_string('changePassword.txt', {'name': user.first_name,'link':link})
            msg_html = render_to_string('changePassword.html', {'name': user.first_name,'link':link})
            send_mail(
                "Change Password",
                msg_plain,
                "earthie@mggroupindia.in",
                [user.email],
                html_message=msg_html,
                fail_silently=False,
            )
            return Response('Email sent',status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"User not found {e}", status=status.HTTP_200_OK)
    return Response("Method not allowed", status=status.HTTP_200_OK)
        


@api_view(('POST',))
def setPassword(req):
    if req.method == 'POST':
        token = req.POST['token']
        pass1 = req.POST['password']
        pass2 = req.POST['confirmPassword']
        try:
            user = User.objects.get(token=token)
            user.set_password(str(pass1))
            user.save()
            msg_plain = render_to_string('resetSuccess.txt', {'name': user.first_name})
            msg_html = render_to_string('resetSuccess.html', {'name': user.first_name})
            send_mail(
                "Password Changed Successfully",
                msg_plain,
                "earthie@mggroupindia.in",
                [user.email],
                html_message=msg_html,
                fail_silently=False,
            )
            return Response("Password Changed Successfully", status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Invalid Link {e}", status=status.HTTP_200_OK)
    return Response("Method not allowed", status=status.HTTP_200_OK)

@api_view(('GET',))
def products(req):
    products = Products.objects.all()
    serializer = ProductSerializer(products, many=True).data
    return Response(data=serializer, status=status.HTTP_200_OK)


@api_view(('GET',))
def newArrivals(req):
    products = Products.objects.all()
    products = products.order_by('-dateUploaded')
    serializer = ProductSerializer(products, many=True).data
    return Response(data=serializer, status=status.HTTP_200_OK)


@api_view(('GET',))
def offers(req):
    products = Products.objects.all()
    products = products.filter(is_in_Offer=True)
    serializer = ProductSerializer(products, many=True).data
    return Response(data=serializer, status=status.HTTP_200_OK)


@api_view(('GET',))
def collections(req):
    allCollections = Collections.objects.all()
    serializer = CollectionsSerializer(allCollections, many=True).data
    return Response(data=serializer, status=status.HTTP_200_OK)



@api_view(('GET',))
def search(req):
    try:
        query = req.GET.get('prod')
        products = Products.objects.filter(tags__icontains=query)
        if products == []:
            return Response({'data':'No products found. Please try again later'}, status=status.HTTP_200_OK)
        serializer = ProductSerializer(products, many=True).data
        return Response(data=serializer, status=status.HTTP_200_OK)
    except:
        return Response({'data':'No products found. Please try again later'}, status=status.HTTP_200_OK)
    



