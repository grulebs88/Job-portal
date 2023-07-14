from django.urls import path
from .views import CandidateList, CandidateCreate, CandidateResume

urlpatterns = [
    path('candidates/', CandidateList.as_view(), name='candidate-list'),
    path('candidates/create/', CandidateCreate.as_view(), name='candidate-create'),
    path('candidates/<int:id>/resume/', CandidateResume.as_view(), name='candidate-resume'),
    
]
