from rest_framework import serializers
from .models import CoverLetter, CoverLetterTemplate

class CoverLetterTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverLetterTemplate
        fields = '__all__'

class CoverLetterSerializer(serializers.ModelSerializer):
    template_details = CoverLetterTemplateSerializer(source='template', read_only=True)

    class Meta:
        model = CoverLetter
        fields = [
            'id', 'title', 'template', 'template_details', 'recipient_name',
            'company_name', 'recipient_address', 'subject',
            'content', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Assigner automatiquement l'utilisateur connecté
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)