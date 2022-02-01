from rest_framework import serializers
from .models import FibonacciResults, FactorialResults, PowResults


class FibonacciResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FibonacciResults
        fields = ['date', 'arg1', 'result']


class FactorialResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactorialResults
        fields = ['date', 'arg1', 'result']


class PowResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PowResults
        fields = ['date', 'arg1', 'arg2', 'result']
