from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, SerializerMethodField, IntegerField
from .models import Activity, UserActivity, UserActivityLog

UserModel = get_user_model()


class ActivitySerializer(ModelSerializer):
    class Meta:
        model = Activity
        fields = (
            "id",
            "name",
            "description",
        )
        read_only_fields = (
            "name",
            "description",
        )


class UserActivityLeaderboardSerializer(ModelSerializer):
    highest_score = IntegerField(min_value=0, max_value=100)

    class Meta:
        model = UserModel
        fields = (
            "id",
            "username",
            "highest_score",
        )


class UserActivitySerializer(ModelSerializer):
    trials_left = SerializerMethodField()
    activity = ActivitySerializer()

    class Meta:
        model = UserActivity
        fields = "__all__"
        read_only_fields = (
            "user",
            "completed",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data: any):
        # assume current user id is 1
        validated_data["user"] = UserModel.objects.get(id=1)
        return super().create(validated_data)
    
    def get_trials_left(self, instance: "UserActivity") -> str:
       return getattr(instance, "trials_left")
    
class UserActivityLogSerializer(ModelSerializer):
    class Meta:
        model = UserActivityLog
        fields = "__all__"
