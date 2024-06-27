from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import StrategySerializer
from .utility import run_strategy, stop_strategy, previous_orders

# Create your views here.

class RunStrategy(APIView):
    def post(self, request, *args, **kwargs):
        print(self.request.data)
        serializer = StrategySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
        response = run_strategy(request.data, str(self.request.user.id))
        return Response(response, status_code=status.HTTP_200_OK)

class StopStrategy(APIView):
    def get(self, *args, **kwargs):
        if not self.kwargs['strategy_id']:
            return Response("strategy_id is required", status_code=status.HTTP_400_BAD_REQUEST)
        response = stop_strategy(self.kwargs['strategy_id'])
        return Response(response, status_code=status.HTTP_200_OK)

class PreviousOrderList(APIView):
    def get(self, request, *args, **kwargs):
        response = previous_orders(str(self.request.user.id))
        if not response:
            return Response({"message": "No Previous order found", "success": True}, status_code=status.HTTP_200_OK)
        return Response({"message": response, "success": True}, status_code=status.HTTP_200_OK)