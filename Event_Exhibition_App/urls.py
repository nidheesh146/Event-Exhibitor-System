from django.urls import path, include
# pyrefly: ignore [missing-import]
from rest_framework.routers import DefaultRouter
from .views import AllocateBadgeAPIView, UploadBatchStatusAPIView, register_view,  BadgeViewSet,GetInvitationAPIView, CompleteRegistrationAPIView, LoginAPIView, CreateBadgeAPIView, CreateExhibitorAPIView, CreateInvitationAPIView, InvitationListAPIView,InvitationViewSet,DashboardAPIView,RegistrationAPIView, MappingListAPIView, BulkDeleteBadgeAPIView,ExportBadgesAPIView, SendInvitationAPIView, TicketTypeAPIView, UploadBatchAPIView, ExhibitorUploadBatchesAPIView, UploadBatchListAPIView, UploadRecordListAPIView, UploadRecordUpdateAPIView, SaveMappingAPIView, exhibitor_dashboard_view, exhibitor_login_page_view, visitor, DeleteUploadRecordAPIView, BulkDeleteUploadRecordAPIView, DeleteSelectedUploadRecordsAPIView

router = DefaultRouter()
router.register(
    r'badges',
    BadgeViewSet,
    basename='badge'
)
router.register(
    r'invitations',
    InvitationViewSet,
    basename='invitation'
)


urlpatterns = [
    
    path(
        'dashboard/',
        DashboardAPIView.as_view()
    ),
    path(
    "register/<uuid:token>/",
    RegistrationAPIView.as_view()
),
    path(
    "badges/bulk-delete/",
    BulkDeleteBadgeAPIView.as_view()
),
    path(
    "badges/export/",
    ExportBadgesAPIView.as_view()
),
     
    path(
    "upload-batch/",
    UploadBatchAPIView.as_view()
),
     
    path(
    "exhibitor-batches/",
    ExhibitorUploadBatchesAPIView.as_view(),
    name="exhibitor-batches"
),
    path(
    "upload-records/",
    UploadRecordListAPIView.as_view()
),
    path(
    "upload-record/<int:record_id>/",
    UploadRecordUpdateAPIView.as_view()
),
    path(
    "upload-record/<int:record_id>/delete/",
    DeleteUploadRecordAPIView.as_view(),
    name="delete-upload-record"
),
    path(
    "upload-records/delete-selected/",
    DeleteSelectedUploadRecordsAPIView.as_view(),
    name="delete-selected-upload-records"
),
    path(
    "upload-records/bulk-delete/",
    BulkDeleteUploadRecordAPIView.as_view(),
    name="bulk-delete-upload-records"
),
    path(
    "upload-batch/<int:batch_id>/mapping/",
    SaveMappingAPIView.as_view()
),
    
    
    path(
    "upload-batch/<int:batch_id>/mapping-list/",
    MappingListAPIView.as_view()
),
    
    path(
    "send-invitation/",
    SendInvitationAPIView.as_view()
),
    
    path(
    "ticket-types/",
    TicketTypeAPIView.as_view()
),
        path("create-badge/", CreateBadgeAPIView.as_view(), name="create-badge"),
        
        path(
    "create-exhibitor/",
    CreateExhibitorAPIView.as_view()
),
        path(
    "create-exhibitor/",
    CreateExhibitorAPIView.as_view(),
    name="create-exhibitor"
),
        
     
path("api/login/", LoginAPIView.as_view(), name="api_login"),
     
    path(
    "exhibitor/",
    exhibitor_dashboard_view,
    name="exhibitor-dashboard"
),
    path(
    "exhibitor-login-page/",
    exhibitor_login_page_view,
    name="exhibitor-login-page"
),
    
     path(
    "visitor/",
    visitor,
    name="visitor"
),
     
     
    path(
    "dashboard.html",
    exhibitor_dashboard_view,
    name="dashboard-html"
),
    
    path(
    "upload-batches/",
    UploadBatchListAPIView.as_view(),
    name="upload-batches"
),
    path(
    "allocate-badges/<int:exhibitor_id>/",
    AllocateBadgeAPIView.as_view(),
    name="allocate-badges"
),
    
    
    
    path(
    "create-invitation/",
    CreateInvitationAPIView.as_view(),
    name="create-invitation"
),



path(
    "invitations/",
    InvitationListAPIView.as_view(),name="invitation-list"
),
     

    path("api/invitation/<uuid:token>/", GetInvitationAPIView.as_view(), name="get-invitation"),

    path("api/register/<uuid:token>/", CompleteRegistrationAPIView.as_view(), name="complete-registration"),
    
    path(
    "register/",
    register_view,
    name="register"
),
    
    path(
    "upload-batch-status/<int:batch_id>/",
    UploadBatchStatusAPIView.as_view(),
),

    
    path('', include(router.urls)),
]
