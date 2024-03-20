from menus.menu_builder.exceptions import MenuGenerationException


def screen_check_decorator(func):
    """
    Checks if the screen type is what is expected
    /right menu_screens function was called/
    """

    def wrapper(*args, **kwargs):
        menu_obj = args[0]
        if menu_obj.menu_type.name != func.__name__:
            raise TypeError(f'Expected: "{menu_obj.menu_type.name}", got: {func.__name__} for {menu_obj}')
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            raise MenuGenerationException(
                error_message=f'Error when generating menus for: {menu_obj}. \n'
                              f'Original error was: {type(e).__name__} -> {str(e)}') from e

        return result

    return wrapper
