from django.urls import path
from .api_views import IncomeRetrieveAPIView, IncomeListAPIView


app_name = 'income'

urlpatterns = [
    path('', IncomeListAPIView.as_view(), name='incomes'),
    path('<int:pk>/', IncomeRetrieveAPIView.as_view(), name='income'),  # If <int:id> is used instead, the
    # 'lookup_field' attribute should be added in .api_views like this: lookup_field = 'id'

]
