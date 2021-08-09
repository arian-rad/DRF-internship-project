from rest_framework.views import APIView
import datetime
from expenses.models import Expense
from rest_framework import status
from rest_framework.response import Response


class ExpenseSummaryStats(APIView):
    def get_amount_for_category(self, expenses_list, category):
        expenses = expenses_list.filter(category=category)
        amount = 0
        for expn in expenses:
            amount += expn.amount
        return {'amount': str(amount)}

    def get(self, request):
        date_today = datetime.date.today()
        last_year = date_today - datetime.timedelta(days=365)
        expenses = Expense.objects.filter(owner=request.user, date__gte=last_year, date__lte=date_today)
        final = {}
        categories = list(set(map(lambda item: item.category, expenses)))
        for expn in expenses:
            for category in categories:
                final[category] = self.get_amount_for_category(expenses, category)
        return Response({'category_data': final}, status=status.HTTP_200_OK)
