from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import HomePageView, UserActivityView, UserActivityLeaderboardView


router = DefaultRouter(trailing_slash=True)
router.register("api/user_activity", UserActivityView, "user_activity")

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('api/leaderboard', UserActivityLeaderboardView.as_view(), name='user_activity_leaderboard'),
] + router.urls