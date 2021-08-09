from django.urls import path
from .api_views import ExpenseSummaryStats

app_name = 'userstats'

urlpatterns = [
    path('expense-category-data/', ExpenseSummaryStats.as_view(), name='expense_summary_category'),
]