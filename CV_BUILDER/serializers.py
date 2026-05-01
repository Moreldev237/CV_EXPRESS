from rest_framework import serializers
from .models import CV, Template, Experience, Education, Skill, Language, Project

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = '__all__'

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'

    def validate(self, data):
        if data.get('end_date') and data.get('start_date'):
            if data['end_date'] < data['start_date']:
                raise serializers.ValidationError({"end_date": "La date de fin ne peut pas être antérieure à la date de début."})
        return data

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

    def validate(self, data):
        if data.get('end_date') and data.get('start_date'):
            if data['end_date'] < data['start_date']:
                raise serializers.ValidationError({"end_date": "La date de fin ne peut pas être antérieure à la date de début."})
        return data

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class CVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        fields = ['id', 'title', 'template', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Assigner l'utilisateur connecté automatiquement
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class CVFullSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la vue 'full' incluant toutes les sections imbriquées."""
    experiences = ExperienceSerializer(many=True, read_only=True)
    educations = EducationSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)
    template_details = TemplateSerializer(source='template', read_only=True)

    class Meta:
        model = CV
        fields = [
            'id', 'title', 'template', 'template_details', 
            'experiences', 'educations', 'skills', 'languages', 'projects',
            'created_at', 'updated_at'
        ]