from django_filters import rest_framework as filters

from wishes.models import Wishes


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class WishFilter(filters.FilterSet):
    name = CharFilterInFilter(field_name='name', lookup_expr='in')
    price = filters.RangeFilter(field_name='price')
    reason = CharFilterInFilter(field_name='reason', lookup_expr='in')
    created_by = CharFilterInFilter(field_name='created_by', lookup_expr='in')

    class Meta:
        model = Wishes
        fields = ['name', 'price', 'created_by', 'reason']
