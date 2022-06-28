from django.urls import path

from .views import (AppointmentCreateApiView, ClientAppointmentListApi,
                    DateAndTimeWorkApiView, LocationListApiView,
                    ScheduleCreateApiView, ScheduleDeleteApiView,
                    ScheduleUpdateApiView, ServiceListApiView,
                    SpecialistAppointmentListApiView,
                    SpecialistDetailScheduleListApiView, SpecialistListApiView,
                    SpecialistScheduleListApiView, UserInfoRetrieveApiView)

urlpatterns = [
    path("specialist/list/", SpecialistListApiView.as_view()),
    path("specialist/schedule/", SpecialistScheduleListApiView.as_view()),
    path("specialist/schedule/create/", ScheduleCreateApiView.as_view()),
    path(
        "specialist/schedule/list/<slug:slug>/",
        SpecialistDetailScheduleListApiView.as_view(),
    ),
    path(
        "specialist/appointment/list/<slug:slug>/",
        SpecialistAppointmentListApiView.as_view(),
    ),
    path("schedule/delete/<int:pk>", ScheduleDeleteApiView.as_view()),
    path("schedule/update/<int:pk>/", ScheduleUpdateApiView.as_view()),
    path("date-work/<int:pk>/", DateAndTimeWorkApiView.as_view()),
    path("client/appointment/list/", ClientAppointmentListApi.as_view()),
    path("user/info/<slug:slug>/", UserInfoRetrieveApiView.as_view()),
    path("create/", AppointmentCreateApiView.as_view()),
    path("location/list/", LocationListApiView.as_view()),
    path("service/list/", ServiceListApiView.as_view()),
]
