from rest_framework import serializers
from .models import Patent

class PatentQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Patent
        fields = '__all__'

class PatentSummarySerializer(serializers.Serializer):
    total_patents               = serializers.IntegerField()
    max_assignee                = serializers.DictField(child=serializers.CharField())
    max_inventor                = serializers.DictField(child=serializers.CharField())
    earliest_filing_date        = serializers.DictField(child=serializers.CharField())
    latest_filing_date          = serializers.DictField(child=serializers.CharField())
    earliest_publication_date   = serializers.DictField(child=serializers.CharField())
    latest_publication_date     = serializers.DictField(child=serializers.CharField())