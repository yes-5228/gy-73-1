from django.urls import path

from . import views


urlpatterns = [
    path("", views.review_list),
    path("orders/<int:order_id>/", views.create_review),
]
