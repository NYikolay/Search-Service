from rest_framework.filters import BaseFilterBackend


class CargoFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if request.query_params.get('miles'):
            ...
        if request.query_params.get('weight'):
            return queryset.filter(weight=request.query_params.get('weight'))
        return queryset
