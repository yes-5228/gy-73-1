from django.urls import path

from . import views


urlpatterns = [
    path("", views.order_list),
    path("<int:order_id>/", views.order_detail),
    path("<int:order_id>/claim/", views.claim_order),
    path("<int:order_id>/assign/", views.assign_order),
]
