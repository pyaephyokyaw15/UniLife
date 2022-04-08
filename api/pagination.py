from rest_framework.pagination import CursorPagination


class CursorSetPagination(CursorPagination):
    page_size = 4
    ordering = 'date_posted'  # '-created' is default
