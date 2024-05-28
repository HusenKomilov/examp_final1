from django.urls import path
from blog import views

urlpatterns = [
    path("last/", views.PostNewListAPIView.as_view()),
    path("watched/", views.PostWatchedListAPIView.as_view()),
    path("recomendation/", views.PostRecomendationListAPIView.as_view()),
    path("wekkly/", views.PostWeeklyListAPIView.as_view()),
    path("month/", views.PostMonthListAPIView.as_view()),
    path("<int:pk>/", views.PostRetriveAPIView.as_view()),
    path("create-post/", views.PostCreateAPIView.as_view()),

    path("comment-create/", views.CommentCreateAPIView.as_view()),
    path("comment/<int:pk>/", views.CommentListAPIView.as_view()),
]
