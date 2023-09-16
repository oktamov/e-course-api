from drf_yasg import openapi

is_popular_param = openapi.Parameter(name="is_popular", in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
