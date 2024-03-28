from django.shortcuts import render
from django.db.models import Max
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from rest_framework import status, response
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import UserActivity, UserActivityLog, do_training
from .serializers import UserActivitySerializer, UserActivityLogSerializer, UserActivityLeaderboardSerializer

UserModel = get_user_model()


class HomePageView(TemplateView):
    template_name = "index.html"


class UserActivityView(GenericViewSet, CreateModelMixin, ListModelMixin):
    serializer_class = UserActivitySerializer
    queryset = UserActivity.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_activity = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return response.Response({
            "status_code": status.HTTP_201_CREATED,
            "message": "Activity registered.",
            "data": self.get_serializer(user_activity).data
        }, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=True, methods=["get"])
    def activity_logs(self, request, *args, **kwargs):
        instance: UserActivity = self.get_object()
        queryset = UserActivityLog.objects.filter(user_activity=instance)

        return response.Response({
            "status_code": status.HTTP_200_OK,
            "message": "Activity Logs retrieved.",
            "data": UserActivityLogSerializer(queryset, many=True).data
        })

    @action(detail=True, methods=["post"])
    def finish_session(self, request, *args, **kwargs):
        instance: UserActivity = self.get_object()

        # check no of trials
        if instance.completed:
            return response.Response(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "Trials has been exceeded",
                    "data": None
                },
                status.HTTP_400_BAD_REQUEST
            )
        
        # generate random score (3 trials)
        score = do_training()
        instance.create_activity_log(score=score)
       
        return response.Response(
            {
                "status_code": status.HTTP_201_CREATED,
                "message": "Training session completed.",
                "data": {
                    "score": score
                },
            },
            status.HTTP_201_CREATED,
        )
    
    def get_queryset(self):
        # assume user id is 1
        return super().get_queryset().filter(user__id=1).order_by('completed')
    

class UserActivityLeaderboardView(APIView):
     def get(self, request, format=None):
        """
        Return a list of top users using their score
        """
        # order users by their highest scores
        users =  UserModel.objects.annotate(
            highest_score=Max('useractivity__user_activity_log__score', default=0)
        ).order_by('-highest_score')

        return response.Response(
            {
                "status_code": status.HTTP_200_OK,
                "message": "User Activity Leaderboard",
                "data": UserActivityLeaderboardSerializer(users, many=True).data,
            },
            status.HTTP_200_OK,
        )
  