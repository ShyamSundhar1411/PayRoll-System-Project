import django_filters
from datetime import datetime
from django.db.models import Value
from django.db.models.functions import ExtractMonth
from .models import Payslip

class MonthFilter(django_filters.FilterSet):
    MONTH_CHOICES = [
        ('', 'Select Month'),
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December'),
    ]

    month = django_filters.ChoiceFilter(
        field_name='month',
        label='Select Month',
        choices=MONTH_CHOICES,
        empty_label=None,
        method='filter_by_month',
    )

    class Meta:
        model = Payslip
        fields = ['month']

    def filter_by_month(self, queryset, name, value):
        if value:
            # Filter by the selected month
            return queryset.annotate(
                salary_month=ExtractMonth('month')
            ).filter(salary_month=int(value))
        else:
            # Return the queryset unfiltered if no month is selected
            return queryset
