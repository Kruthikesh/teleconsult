from django.contrib import admin
from apps.tcd.models import *

admin.site.register(DoctorSuggestion)
admin.site.register(TCD)
admin.site.register(PatientProblem)
admin.site.register(PatientProblemReview)
admin.site.register(PatientReviewImage)
admin.site.register(PatientReviewVideo)
