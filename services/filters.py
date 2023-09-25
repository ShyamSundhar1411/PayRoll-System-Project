import django_filters
from datetime import datetime
from django.db.models import Q
from django.db.models.functions import ExtractMonth
from .models import Payslip, Employee
from django import forms

class MonthFilter(django_filters.FilterSet):
    MONTH_CHOICES = [
        ('', 'Select Month'),
        ('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'),
        ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'),
        ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December'),
    ]

    month = django_filters.ChoiceFilter(
        field_name='month',
        label='Select Month',
        choices=MONTH_CHOICES,
        empty_label=None,
        method='filter_by_month',
    )

        # Add a filter field for the year
    year = django_filters.NumberFilter(
        field_name='year',
        label='Select Year',
        lookup_expr='exact',
    )

    class Meta:
        model = Payslip
        fields = ['month','year']

    def filter_by_month(self, queryset, name, value):
        if value:
            # Filter by the selected month
            return queryset.filter(month=value)
        else:
            # Return the queryset unfiltered if no month is selected
            return queryset

class EmployeeFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='filter_search',
        label='Search',
    )

    class Meta:
        model = Employee
        fields = []

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(emp_name__icontains=value) |
            Q(emp_code__icontains=value) |
            Q(department__icontains=value) |
            Q(basic_pay__icontains=value) |
            Q(sa__icontains=value) |
            Q(hra__icontains=value) |
            Q(pra_gain__icontains=value) 
        )