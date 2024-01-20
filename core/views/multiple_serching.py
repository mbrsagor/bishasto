from rest_framework.response import Response
from rest_framework import views, status

from utils import response


class MultipleSerching(views.APIView):
    def get(self, request):
        account = self.request.query_params.get('account')
        date = self.request.query_params.get('date')
        end_date = self.request.query_params.get('end_date')
        types = self.request.query_params.get('types')

        # Transfer
        if types == '1':
            transfer_qs = Transfer.objects.filter(store=self.request.user.storeOwner)
            if account:
                transfer_qs = transfer_qs.filter(Q(account_from=account))
            if date:
                transfer_qs = transfer_qs.filter(Q(date=date))
            transfer_serializer = serializers.TransferUtilsSerializer(transfer_qs, many=True).data
            return Response(response.prepare_success_list_response(messages.DATA_RETURN, transfer_serializer),
                            status=status.HTTP_200_OK)

        # Expense
        elif types == '2':
            expense_qs = Expense.objects.filter(store=self.request.user.storeOwner)
            if account:
                expense_qs = expense_qs.filter(Q(account_id=account))
            if date:
                expense_qs = expense_qs.filter(Q(created_date=date))
            serializer = expense_serializer.ExpenseUtilsSerializer(expense_qs, many=True).data
            return Response(response.prepare_success_list_response(messages.DATA_RETURN, serializer),
                            status=status.HTTP_200_OK)

        # Income
        elif types == '3':
            income_qs = Income.objects.filter(store=self.request.user.storeOwner)
            if account:
                income_qs = income_qs.filter(Q(account_id=account))
            if date:
                income_qs = income_qs.filter(Q(date=date))
            income_serializer = serializers.IncomeUtilsSerializer(income_qs, many=True).data
            return Response(response.prepare_success_list_response(messages.DATA_RETURN, income_serializer),
                            status=status.HTTP_200_OK)

        # Pay
        elif types == '4':
            pay_qs = Pay.objects.filter(store=self.request.user.storeOwner)
            if account:
                pay_qs = pay_qs.filter(account_id=account)
            if date:
                pay_qs = pay_qs.filter(Q(date=date))
            pay_serializer = serializers.PayUtilsSerializer(pay_qs, many=True).data
            return Response(response.prepare_success_list_response(messages.DATA_RETURN, pay_serializer),
                            status=status.HTTP_200_OK)

        # Purchase
        elif types == '5':
            purchase_qs = Purchase.objects.filter(store=self.request.user.storeOwner)
            if account:
                purchase_qs = purchase_qs.filter(account_id=account)
            if date:
                purchase_qs = purchase_qs.filter(Q(date=date))
            if date and end_date is not None:
                purchase_qs = purchase_qs.filter(date__range=[date, end_date])
            purchase_serializer = serializers.PurchaseUtilsSerializer(purchase_qs, many=True).data
            return Response(response.prepare_success_list_response(messages.DATA_RETURN, purchase_serializer),
                            status=status.HTTP_200_OK)

