
def is_user_authenticated(request):
    """
        Check if the session exist inside the specified
        request

        :param request: The request being analyzed
    """
    return request.session.session_key

