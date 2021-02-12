from .serializers import UserSerializer
from rest_framework import generics, status
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UpdateProfileSerializer, ChangePasswordSerializer
from rest_framework.decorators import api_view, permission_classes

User = get_user_model()

@api_view(['GET'])
@permission_classes((AllowAny,))
def home(request):
    return Response('Welcome to Chahapura API', status=status.HTTP_200_OK)

class UserDetail(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserList(generics.ListAPIView):
    serializer_class = UserSerializer
    model = serializer_class.Meta.model
    permission_classes = (DjangoModelPermissions,)

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = [
        AllowAny, # Or anon users can't register
    ]
    serializer_class = UserSerializer


class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = UpdateProfileSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance.first_name = request.data.get("first_name")
            instance.last_name = request.data.get("last_name")
            instance.contact = request.data.get("contact")

            instance.save()

            return Response({
                'status': 'success',
                'code': status.HTTP_200_OK,
                'data': serializer.data,
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(generics.UpdateAPIView):
        """
        An endpoint for changing password.
        """
        serializer_class = ChangePasswordSerializer
        model = User
        permission_classes = (IsAuthenticated,)

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
