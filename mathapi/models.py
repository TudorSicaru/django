from django.db import models


# NOTE: Storing the result as a TextField to avoid OverflowError

class FibonacciResults(models.Model):
    """A table that stores the results of different 'fibonacci' function calls"""
    date = models.DateTimeField(auto_now_add=True)
    arg1 = models.IntegerField(blank=False)
    result = models.TextField(blank=True)
    ret_code = models.IntegerField()


class FactorialResults(models.Model):
    """A table that stores the result 'factorial' function calls"""
    date = models.DateTimeField(auto_now_add=True)
    arg1 = models.IntegerField(blank=False)
    result = models.TextField(blank=True)
    ret_code = models.IntegerField()


class PowResults(models.Model):
    """A table that stores the result of 'pow' function calls"""
    date = models.DateTimeField(auto_now_add=True)
    arg1 = models.FloatField(blank=False)
    arg2 = models.FloatField(blank=False)
    result = models.TextField(blank=True)
    ret_code = models.IntegerField()
