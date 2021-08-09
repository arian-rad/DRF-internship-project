from django.urls import path
from .api_views import ExpenseSummaryStats, IncomeSourcesSummaryStats

app_name = 'userstats'

urlpatterns = [
    path('expense-category-data/', ExpenseSummaryStats.as_view(), name='expense_summary_category'),
    path('income-source-data/', IncomeSourcesSummaryStats.as_view(), name='income_summary_source'),
]
