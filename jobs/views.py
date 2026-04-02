from django.shortcuts import render
from rest_framework import generics, filters
from .models import JobPosting
from .serializers import JobPostingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import JobPosting
from .serializers import JobPostingSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class JobPostingList(generics.ListAPIView):
    queryset = JobPosting.objects.all().order_by('-created_at')
    serializer_class = JobPostingSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        location = self.request.query_params.get('location')
        if location:
            queryset = queryset.filter(location__icontains=location)
        return queryset

class JobPostingDetail(generics.RetrieveAPIView):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer

class PremiumJobsOverview(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user_membership = 'basic'
        if request.user.is_authenticated:
            user_membership = getattr(request.user.profile, 'membership_type', 'basic')

        all_jobs = JobPosting.objects.all().order_by('-created_at')
        serializer = JobPostingSerializer(all_jobs, many=True, context={'request': request})

        # Count Premium jobs (for teaser)
        premium_job_count = all_jobs.count()

        if user_membership == 'premium':
            return Response({
                "membership": "premium",
                "jobs": serializer.data
            })
        else:
            return Response({
                "membership": "basic",
                "premium_job_count": premium_job_count,
                "jobs": serializer.data  # Masked automatically by serializer
            })
class UpgradeToPremium(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_profile = getattr(request.user, 'profile', None)
        if not user_profile:
            return Response({"detail": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

        if user_profile.membership_type == 'premium':
            return Response({"detail": "You are already a Premium member."}, status=status.HTTP_400_BAD_REQUEST)

        # Upgrade the user
        user_profile.membership_type = 'premium'
        user_profile.save()

        return Response({"detail": "Successfully upgraded to Premium!"})       