def menu_context(request):
    return {
        'is_staff': request.user.is_staff,
    }