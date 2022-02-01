"""This module defines helpers used by the views"""
import math
import sys


def calculate_hash(operation_name, operation_arguments) -> str:
    """Function that takes a string and a list of args and 'calculates' a 'hash' of them (just appending strings)
    to uniquely identify a call for the specific operation

    :param operation_name: Name of the operation (one of ['pow', 'fib', 'factorial']
    :type operation_name: str
    :param operation_arguments: A list of argument(s), depending on operation being executed
    :type operation_arguments: List[float]

    :return: A string which is the hash of all of the above
    :rtype: str
    """
    arg_string = ','.join(map(str, operation_arguments))
    return operation_name + arg_string


def retrieve_result_from_db(inst, arguments):
    """Try to retrieve a result 'cached' in the database, or return error code

    :param inst: Instance of a subclass of django's models.Model
    :type inst: models.Model
    :param arguments: The list of the arguments provided for the operation
    :type arguments: List[float]
    :return: A tuple consisting of the ret_code and the result of the operation. The ret_code will be -1 when the
    database entry is not found
    :rtype: Tuple(int, float)
    """
    try:
        # Allow variable number of arguments as long as they follow the convention arg1, arg2, arg3...etc
        filters = {}
        for idx, arg in enumerate(arguments, 1):
            filters[f'arg{idx}'] = arg
        found_obj = inst.objects.get(**filters)
        ret_code = found_obj.ret_code  # Preserving the ret_code of the original operation
        result = found_obj.result
    except inst.DoesNotExist:
        ret_code, result = -1, ''
    return ret_code, result


def perform_math_operation(operation, *arguments):
    """Dynamically selects one of the available operations and executes it with the provided arguments

    :param operation: Name of the operation (one of ['power', 'fibonacci', 'factorial']
    :type operation: str
    :param arguments: A list of argument(s), depending on operation being executed
    :type arguments: List[float]
    :return: A tuple consisting of the ret_code (0 for success and 1 for errors) and the result of the operation
    :rtype: Tuple(int, float)
    """
    try:
        # 'operation' is constrained by the 'choices' in models, so we should never have AttributeError here
        operation = getattr(sys.modules[__name__], operation)
        return 0, operation(*arguments)
    except AttributeError:
        return 1, f"'{operation}' is not a supported/implemented operation"
    except (OverflowError, TypeError, ValueError) as err:
        return 1, str(err)


def power(base, exponent):
    """Calculates the value of base^exponent.

    :param base: A float representing the base of the power function
    :type base: float
    :param exponent: A float - the exponent of the power function
    :type exponent: float
    :return: The result of the power function
    :rtype: float
    """
    return math.pow(base, exponent)


def factorial(integer):
    """Calculates the factorial of the provided integer

    :param integer: The input of the factorial function
    :type integer: int
    :return: A number - the factorial of the integer
    :rtype: int
    """
    return math.factorial(integer)


def fibonacci(integer):
    """Calculates the integer-th number of the fibonacci sequence. Not ideal implementation, but at least we don't
    run in RecursionError.

    :param integer: The input of the fibonacci function
    :type integer: int
    :return: A number - the integer-th number of the fibonacci sequence
    :rtype: int
    """
    if integer < 0:
        raise ValueError(f'The argument: {integer} should be a positive integer!')
    a, b = 0, 1
    for _ in range(integer):
        a, b = b, a + b
    return a
