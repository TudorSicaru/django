from django.contrib import admin
from .models import FactorialResults, FibonacciResults, PowResults


admin.site.register(FactorialResults)
admin.site.register(FibonacciResults)
admin.site.register(PowResults)
