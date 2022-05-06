
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from accounts.models import User
from .serializers import UserLoginSerializer, UserSerializer
from .services import EmailService


@api_view(["POST", ])
@permission_classes([AllowAny, ])
def create_user_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")
        print(password)
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            user = User.objects.create_user(email=email, password=password)
            # user.set_password(password)
            # user.save()
    else:
        return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
    return Response(
        {
            "message": "Account created",
            "email": user.email,
        },
        status=status.HTTP_201_CREATED
    )


@api_view(["POST", ])
def login_view(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user.save()

        return Response(
            {
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
            },
            status=status.HTTP_200_OK
        )
    else:
        try:
            message = serializer.errors['non_field_errors'][0]
        except (IndexError, KeyError) as e:
            message = "Some random message I don't know y"

    return Response({'message': message}, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):

    permission_classes(IsAuthenticated)

    def post(self, request):
        print(request.data.dict())
        try:
            profile = Profile.objects.get(user=request.user)
            profile.delete()
        except ObjectDoesNotExist:
            pass
        profile = Profile(user=request.user, **request.data.dict())
        profile.save()
        return Response({"message": "Profile Updated"}, status=status.HTTP_200_OK)

    def get(self, request):
        user = request.user
        try:
            profile = Profile.objects.get(user=user)
        except ObjectDoesNotExist:
            return Response({"message": "user profile doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

class OtpView(APIView):
    def get(self,request):
        user=request.user
        if user.otp is None:
            user.generateotp()
        print("OTP is ")
        print (user.otp)
        EmailService.send_otp_to_user(user)
        return Response(
            {"message": "OTP send successfully"},
            status=status.HTTP_200_OK
        )
    def post(self, request):
        user=request.user
        otp=request.data.get('otp')
        print(f"otp from verify is {otp} and type is {type(otp)}")
        print(f"User otp is {user.otp} and type is {type(user.otp)}")
        if timezone.now() > user.otp_generated_at + timezone.timedelta(hours=5.00):
            return Response({"message": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)
        
        if otp == user.otp:
            user.verifyotp()
            
            return Response(
                {"message": "Email verification successfull"},
                status=status.HTTP_200_OK
            )
        else:
            return Response({"message": "Wrong OTP!"}, status=status.HTTP_400_BAD_REQUEST)

class RetryOtpView(APIView):
    def get(self,request):
        user=request.user
        user.otp=None
        user.generateotp()
        EmailService.send_otp_to_user(user)
        return Response(
            {"message": "New OTP has been sent to your email"},
            status=status.HTTP_200_OK
        )

class UsernameView(APIView):
    def post(self, request):
        user = request.user
        tempname = request.data.get('username')
        try:
            User.objects.get(username=tempname)
            
            return Response({"message": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            user.username = tempname
            print(f'username from view is {tempname}')
            user.save()
            return Response({"message": "Username updated"}, status=status.HTTP_200_OK)

