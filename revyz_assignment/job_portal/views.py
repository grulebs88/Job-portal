from django.shortcuts import render

# Create your views here.
import os
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.http import FileResponse, HttpResponseNotFound
from django.shortcuts import render
from .models import Candidate,  TechSkill
from .serializers import CandidateSerializer
from django.conf import settings
import boto3


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class CandidateList(generics.ListAPIView):
    queryset = Candidate.objects.all().order_by('name')
    serializer_class = CandidateSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        location = self.request.query_params.get('location', None)
        tech_skills = self.request.query_params.get('tech_skills', None)
        if location:
            queryset = queryset.filter(location__iexact=location)
        if tech_skills:
            queryset = queryset.filter(tech_skills__name__in=tech_skills).distinct()
        return queryset[:50]

'''
class CandidateCreate(generics.CreateAPIView):
    serializer_class = CandidateSerializer

    def post(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            candidate = serializer.save()

            # Generate resume and store in S3
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,)
            file_name = f'candidate_{candidate.id}_resume.pdf'
            file_content = f"Name: {candidate.name}\nEmail: {candidate.email}\nPhone Number: {candidate.phone_number}\nCity: {candidate.location}\nTech Skills: {candidate.tech_skills}"
            s3_client.put_object(Bucket='candidatecv', Key=file_name, Body=file_content.encode())

            # Encrypt the file
            s3_client.put_object_acl(Bucket='candidatecv', Key=file_name, ACL='private')

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

'''

from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

class CandidateCreate(generics.CreateAPIView):
    serializer_class = CandidateSerializer

    def post(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            candidates = serializer.save()

            # Generate resume and store in MySQL database
            for candidate in candidates:
                buffer = BytesIO()
                doc = SimpleDocTemplate(buffer, pagesize=letter)
                styles = getSampleStyleSheet()
                story = []
                story.append(Paragraph(f'Name: {candidate.name}', styles['Normal']))
                story.append(Paragraph(f'Email: {candidate.email}', styles['Normal']))
                story.append(Paragraph(f'Phone Number: {candidate.phone_number}', styles['Normal']))
                story.append(Paragraph(f'City: {candidate.location}', styles['Normal']))
                tech_skills = ', '.join([skill.name for skill in candidate.tech_skills.all()])
                story.append(Paragraph(f'Tech Skills: {tech_skills}', styles['Normal']))
                doc.build(story)
                pdf = buffer.getvalue()
                buffer.close()
                candidate.resume = pdf
                candidate.save()

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CandidateResume(generics.RetrieveAPIView):
    queryset = Candidate.objects.all()
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        candidate = self.get_object()
        resume = candidate.resume
        if not resume:
            return HttpResponseNotFound('Resume not found')
        file_path = f'/tmp/resumes/{candidate.id}.pdf'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(resume)
        response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={candidate.name}.pdf'
        return response