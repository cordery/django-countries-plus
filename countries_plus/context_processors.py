def add_request_country(request):
    """Add 'country' to the request context.  Requires countries_plus middleware."""
    return {'country': getattr(request, 'country', None)}
