from rest_framework import serializers
from .models import Candidate, TechSkill

class TechSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechSkill
        fields = ['name']

class CandidateSerializer(serializers.ModelSerializer):
    tech_skills = TechSkillSerializer(many=True)
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'address', 'phone_number', 'email', 'location', 'tech_skills']

