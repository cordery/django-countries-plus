# requires countries_plus middleware
def add_request_country(request):
    return {'country': request.country}
