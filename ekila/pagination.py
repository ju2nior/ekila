from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 20


class CustomPagination(PageNumberPagination):
    page = DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        try:
            current_page = int(self.request.GET.get("page", DEFAULT_PAGE))
        except ValueError:
            current_page = DEFAULT_PAGE

        try:
            current_page_size = int(self.request.GET.get("page_size", self.page_size))
        except ValueError:
            current_page_size = self.page_size

        return Response(
            {
                "total": self.page.paginator.count,
                "page": max(current_page, DEFAULT_PAGE),
                "page_size": max(current_page_size, DEFAULT_PAGE_SIZE),
                "total_pages": self.page.paginator.num_pages,
                "results": data,
            }
        )
