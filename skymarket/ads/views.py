from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import pagination, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from ads.filters import AdFilter
from ads.models import Ad, Comment
from ads.permissions import IsOwner, IsAdmin
from ads.serializers import AdSerializer, AdDetailSerializer, CommentSerializer


class AdPagination(pagination.PageNumberPagination):
    page_size = 4


class AdViewSet(viewsets.ModelViewSet):
    method = None
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    pagination_class = AdPagination
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdFilter

    def get_queryset(self):
        if self.action == "me":
            return Ad.objects.filter(author=self.request.user).all()
        return Ad.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)

    def get_serializer_class(self):
        if self.action in ["list", "me"]:
            return AdSerializer
        elif self.action in ["create", "destroy", "update", "partial_update", "retrieve"]:
            return AdDetailSerializer

    def get_permissions(self):
        permission_classes = [AllowAny]
        if self.action in ["retrieve"]:
            permission_classes = [AllowAny]
        elif self.action in ["create", "destroy", "update", "partial_update", "me"]:
            permission_classes = [IsAdmin, IsOwner]
        return tuple(permission() for permission in permission_classes)

    @action(method='GET', detail=False)
    def me(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        ad_id = self.kwargs.get("ad_pk")
        ad = get_object_or_404(Ad, pk=ad_id)
        return ad.comments.all()

    def perform_create(self, serializer):
        ad_id = self.kwargs.get("ad_pk")
        ad = get_object_or_404(Ad, pk=ad_id)
        user = self.request.user
        serializer.save(author=user, ad=ad)

    def get_permissions(self):
        permission_classes = [AllowAny]
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        elif self.action in ["create"]:
            permission_classes = [IsAuthenticated]
        elif self.action in ["destroy", "update", "partial_update"]:
            permission_classes = [IsAdmin, IsOwner]
        return tuple(permission() for permission in permission_classes)
