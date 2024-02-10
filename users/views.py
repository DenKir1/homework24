from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.permissions import IsOwner
from users.serializers import UserSerializer, MyTokenObtainPairSerializer, UserOtherSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = super().perform_create(serializer)

        if user is not None:
            password = self.request.data['password']
            user.set_password(password)
            user.save()

        return user

    def get_permissions(self):
        permission_classes = []
        if self.action == 'retrieve' or self.action == 'list':
            permission_classes = [IsAuthenticated]
        if self.action == 'update' or self.action == 'destroy':
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        # print(self.__dict__)
        if self.request.user:  # не нашел с кем его сравнить в сериализаторе
            return UserSerializer
        return UserOtherSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
