from django.urls import path
from .api_views import ExpenseRetrieveAPIView, ExpenseListAPIView


app_name = 'expenses'

urlpatterns = [
    path('', ExpenseListAPIView.as_view(), name='expenses'),
    path('<int:id>/', ExpenseRetrieveAPIView.as_view(), name='expense'),

]