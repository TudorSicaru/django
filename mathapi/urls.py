from django.urls import path
from .views import FibonacciView, FactorialView, PowerView

urlpatterns = [
    path('fibonacci/', FibonacciView.as_view()),
    path('factorial/', FactorialView.as_view()),
    path('pow/', PowerView.as_view())
    ]
