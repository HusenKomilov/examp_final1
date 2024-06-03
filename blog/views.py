from rest_framework import generics, permissions, viewsets
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta, datetime
from blog import models, serializers


class PostNewListAPIView(generics.ListAPIView):
    queryset = models.Posts.objects.filter(is_published=True).order_by(
        "-created_at").select_related("category", "author").prefetch_related("tags")
    serializer_class = serializers.PostSerializer


class PostWatchedListAPIView(generics.ListAPIView):
    queryset = models.Posts.objects.filter(is_published=True).order_by(
        "-watched").select_related("category", "author").prefetch_related("tags")
    serializer_class = serializers.PostSerializer


class PostRecomendationListAPIView(generics.ListAPIView):
    queryset = models.Posts.objects.filter(Q(is_recomendation=True) & Q(is_published=True)).order_by(
        "?").select_related("category", "author").prefetch_related("tags")
    serializer_class = serializers.PostSerializer


class PostWeeklyListAPIView(generics.ListAPIView):
    queryset = models.Posts.objects.filter(is_published=True).order_by(
        "?").select_related("category", "author").prefetch_related("tags")
    serializer_class = serializers.PostSerializer

    def get_queryset(self):
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=7)
        return super().get_queryset().filter(created_at__range=[start_of_week, end_of_week])


class PostMonthListAPIView(generics.ListAPIView):
    queryset = models.Posts.objects.filter(is_published=True).order_by(
        "?").select_related("category", "author").prefetch_related("tags")
    serializer_class = serializers.PostSerializer

    def get_queryset(self):
        now = timezone.now()
        start_of_month = datetime(now.year, now.month, 1)
        if now.month == 12:
            start_of_next_month = datetime(now.year + 1, 1, 1)
        else:
            start_of_next_month = datetime(now.year, now.month + 1, 1)
        return super().get_queryset().filter(created_at__gte=start_of_month, created_at__lt=start_of_next_month)


class PostCreateAPIView(generics.GenericAPIView):
    queryset = models.Posts.objects.all().select_related("category", "author").prefetch_related("tags")
    serializer_class = serializers.PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostRetriveAPIView(generics.RetrieveAPIView):
    queryset = models.Posts.objects.filter(is_published=True).select_related(
        "category", "author").prefetch_related("tags")
    serializer_class = serializers.PostSerializer

    def get_object(self):
        obj = super().get_object()
        obj.watched += 1
        obj.save()
        return obj


class CommentCreateAPIView(generics.GenericAPIView):
    queryset = models.Comments.objects.all().select_related("posts", "user")
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        serializer.user = self.request.user
        serializer.save()


class CommentListAPIView(generics.ListAPIView):
    queryset = models.Comments.objects.all().select_related("posts", "user")
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs["pk"]
        a = models.Comments.objects.filter(post_id=post_id)
        return a
