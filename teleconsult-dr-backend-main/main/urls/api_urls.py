from django.urls import path
from django.conf.urls.static import static

from apps.tcd.api_views import *
from apps.user.api_views import *

app_name = 'api_urls'

urlpatterns = [
    path('login', LoginAPI.as_view(), name='api_login'),
    path('signup', SignUpAPI.as_view(), name='api_signup'),
    path('logout', LogoutAPI.as_view(), name='api_logout'),
    path('profile', ProfileAPI.as_view(), name='api_profile'),

    path('tcd', TCDAPI.as_view(), name='get_all_tcds_for_user'),
    path('tcd/<slug:tcd_id>', TCDAPI.as_view(), name='get_tcd'),
    path('tcd/<slug:tcd_id>/feedback', TCDFeedbackAPI.as_view(), name='create_tcd_feedback'),
    path('feedback/<slug:feedback_id>', TCDFeedbackAPI.as_view(),
         name='get_patient_review'),
    path('problem-explanation/<slug:problem_explanation_id>', PatientProblemExplainationAPI.as_view(),
         name='get_problem_explanation'),

    path('problem-explanation/<slug:problem_id>/doctor-suggestion', DoctorResponseAPI.as_view(),
         name='doctor_Response'),

    path('doctor-response/<slug:doctor_response_id>', DoctorResponseAPI.as_view(),
         name='get_doctor_response'),

    path('user/ratings-reviews', UserRatingsAndReviewsAPI.as_view(), name='get_tcd_reviews_for_user')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
