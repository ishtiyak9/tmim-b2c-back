from rest_framework import serializers
from checklist.models import *

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasklist
        fields = ['id','name','created_by', 'updated_by']
        extra_kwarg = {
            'name': {
                "required": True,
                "error_messages": { "required": "Please provide  name of the task" }
            },

        }

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.updated_by = validated_data.get('updated_by', instance.updated_by)
        instance.save()
        return instance

class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checklist
        fields = ['id','tasklist', 'title', 'status','complete','customer','created_by', 'updated_by']

    #
    # tasklist = serializers.SerializerMethodField('get_tasklist')
    #
    # def get_tasklist(self, obj):
    #     return obj.tasklist.name