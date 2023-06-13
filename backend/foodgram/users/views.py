from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import Subscription
from recipes.serializers import AuthorSerializer, SubscriptionSerializer
from api.views import StandartResultsSetPagination
from users.models import User


class PaginatedUserViewSet(UserViewSet):
    pagination_class = StandartResultsSetPagination

    @action(detail=False,
            methods=['GET', ],
            permission_classes=[permissions.IsAuthenticated, ]
            )
    def subscriptions(self, request):
        subscriptions = Subscription.objects.filter(user=request.user)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True,
            methods=['POST', 'DELETE', ],
            permission_classes=[permissions.IsAuthenticated, ]
            )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        if user == author:
            return Response(
                {"errors": "Нельзя подписаться на себя!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        subscription = Subscription.objects.filter(
            user=user,
            author=author
        )

        if request.method == 'POST':
            if subscription.exists():
                return Response(
                    {"errors": "Вы уже подписаны на этого автора"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            new_subscription = Subscription.objects.create(
                user=user,
                author=author
            )
            serializer = SubscriptionSerializer(new_subscription)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not subscription.exists():
                return Response(
                    {"errors": "Вы не подписаны на этого автора"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            subscription.delete()
            return Response(
                {"errors": "Вы успешно отписаны"},
                status=status.HTTP_204_NO_CONTENT
            )
