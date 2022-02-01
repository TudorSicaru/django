"""This module contains the views which implement the server responses to client requests
"""
import logging

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from .models import models, FibonacciResults, FactorialResults, PowResults
from .serializers import FactorialResultsSerializer, FibonacciResultsSerializer, PowResultsSerializer
from .helpers import perform_math_operation, calculate_hash, retrieve_result_from_db

from django.core.cache import cache

logger = logging.getLogger('django.mathapi')


class GenericOperationView(APIView):
    model_class = models.Model
    serializer_class = serializers.ModelSerializer
    math_operation = None

    def get(self, request):
        """Standard response page to use POST if you want to interact with the RESTAPI interface"""
        return Response(
            f'The restapi for {self.math_operation} is only accessible through the http POST method',
            status.HTTP_200_OK
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            args = self._build_args_list(serializer)

            # Calculate the "hash" of the operation string and its arguments
            op_hash = calculate_hash(self.math_operation, args)

            if op_hash in cache:
                logger.info(f"Cache hit for operation '{self.math_operation}'!")
                ret_code, result = cache.get(op_hash)
            elif (ret := retrieve_result_from_db(self.model_class, args))[0] != -1:
                logger.info(f"Found the result of the operation '{self.math_operation}' in the database!")
                ret_code, result = ret
            else:
                logger.info(f"Performing '{self.math_operation}'!")
                ret_code, result = perform_math_operation(self.math_operation, *args)
                serializer.validated_data['ret_code'] = ret_code
                serializer.validated_data['result'] = result
                serializer.save()
            # This is only so that the response contains the result (when the result is cached or in db)
            # The convention for REST is to return the entire obj when the operation is successful
            serializer.validated_data['ret_code'] = ret_code
            serializer.validated_data['result'] = result
            cache.set(op_hash, (ret_code, result))
        else:
            logger.error(f'Data validation failed!\n{serializer.errors}')
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        if not ret_code:
            return Response(serializer.validated_data, status.HTTP_200_OK)

        logger.error(f"Operation failed!\n{serializer.validated_data}")
        return Response(result, status.HTTP_400_BAD_REQUEST)

    def _build_args_list(self, serializer_inst):
        """This helper method builds the list of arguments (1 or 2 args). It's required because subclasses of
        this class may need to either reimplement it or extend this method in order to support variable length of
        arguments.

        :param serializer_inst: Instance of a serializer class
        :type serializer_inst: serializers.ModelSerializer
        :return: The list of args
        :rtype: List
        """
        if self.serializer_class in [FactorialResultsSerializer, FibonacciResultsSerializer]:
            args = [serializer_inst.validated_data['arg1']]
        else:
            args = [serializer_inst.validated_data['arg1'], serializer_inst.validated_data['arg2']]
        return args


class FibonacciView(GenericOperationView):
    model_class = FibonacciResults
    serializer_class = FibonacciResultsSerializer
    math_operation = 'fibonacci'


class FactorialView(GenericOperationView):
    model_class = FactorialResults
    serializer_class = FactorialResultsSerializer
    math_operation = 'factorial'


class PowerView(GenericOperationView):
    model_class = PowResults
    serializer_class = PowResultsSerializer
    math_operation = 'power'
