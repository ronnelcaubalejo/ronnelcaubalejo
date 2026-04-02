from django.urls import path
from .views import JobPostingList, JobPostingDetail, PremiumJobsOverview
from .views import UpgradeToPremium

urlpatterns = [
    path('jobs/', JobPostingList.as_view(), name='job-list'),
    path('jobs/<int:pk>/', JobPostingDetail.as_view(), name='job-detail'),
    path('premium-overview/', PremiumJobsOverview.as_view(), name='premium-overview'),
     path('upgrade/', UpgradeToPremium.as_view(), name='upgrade-to-premium'),
]