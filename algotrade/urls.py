from django.urls import path
from .views import (
    RunStrategy,
    StopStrategy,
    PreviousOrderList,
)

urlpatterns = [
    path('start/', RunStrategy.as_view(), name="start"),
    path('stop/', StopStrategy.as_view(), name="stop"),
    path('order-history/', PreviousOrderList.as_view(), name="order_history"),
]