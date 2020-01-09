from guardian.utils import get_anonymous_user


class GuardianAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_anonymous:
            pass
            #request.user = get_anonymous_user()

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
