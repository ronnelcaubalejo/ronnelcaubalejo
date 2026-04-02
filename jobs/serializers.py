from rest_framework import serializers
from .models import JobPosting

class JobPostingSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField()
    salary_range = serializers.SerializerMethodField()
    application_link = serializers.SerializerMethodField()

    class Meta:
        model = JobPosting
        fields = '__all__'

    def get_user_membership(self):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return 'basic'
        return getattr(request.user.profile, 'membership_type', 'basic')

    def get_company_name(self, obj):
        return obj.company_name if self.get_user_membership() == 'premium' else '🔒 Premium Feature'

    def get_salary_range(self, obj):
        return obj.salary_range if self.get_user_membership() == 'premium' else '🔒 Premium Feature'

    def get_application_link(self, obj):
        return obj.application_link if self.get_user_membership() == 'premium' else '🔒 Premium Feature'