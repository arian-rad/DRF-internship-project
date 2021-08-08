from django.urls import path
from .api_views import ExpenseRetrieveAPIView, ExpenseListAPIView


app_name = 'expenses'

urlpatterns = [
    path('', ExpenseListAPIView.as_view(), name='expenses'),
    path('<int:pk>/', ExpenseRetrieveAPIView.as_view(), name='expense'),  # If <int:id> is used instead, the
    # 'lookup_field' attribute should be added in .api_views like this: lookup_field = 'id'

]
