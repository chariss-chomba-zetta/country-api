import os

# General screen settings
import os

INPUT_SCREEN_NAME = 'input_screen'
MENU_SCREEN_NAME = 'menu_screen'
INITIAL_SCREEN_NAME = 'initial_screen'
QUIT_SCREEN_NAME = 'quit_screen'
FUNCTION_SCREEN_NAME = 'function_screen'
ROUTER_SCREEN_NAME = 'router_screen'

ALL_SCREEN_TYPES = [
    INITIAL_SCREEN_NAME,
    INPUT_SCREEN_NAME,
    QUIT_SCREEN_NAME,
    FUNCTION_SCREEN_NAME,
    MENU_SCREEN_NAME,
    ROUTER_SCREEN_NAME,
]

VISIBLE_USER_SCREEN_TYPES = [INPUT_SCREEN_NAME, MENU_SCREEN_NAME, INITIAL_SCREEN_NAME]

DEFAULT_LANGUAGE_CODE = 'en'
LANGUAGE_SUPPORT_SCREENS = [INPUT_SCREEN_NAME, QUIT_SCREEN_NAME, MENU_SCREEN_NAME]
DEFAULT_ERROR_MESSAGE = os.environ.get(
    'DEFAULT_ERROR_MESSAGE',
    'Dear customer, we are unable to process your request now. Try again later.',
)

# Screen navigations
PIN_RESET_SCREEN = os.environ.get('PIN_RESET_SCREEN', 'PinResetIDNumberScreen')
HOME_MENU_SCREEN = os.environ.get('HOME_MENU_SCREEN', 'MainMenuScreen')

NAVIGATION_BACK_INPUT = '0'
NAVIGATION_HOME_INPUT = '00'
NAVIGATION_BACK_TYPE = 'back'
NAVIGATION_HOME_TYPE = 'home'
NAVIGATION_KEY = 'navigation'  # used for REDIS caching as well

BACK_NAVIGATION_TEXT_FALLBACK = 'Back'
MAIN_MENU_NAVIGATION_TEXT_FALLBACK = 'Main Menu'
PIN_RESET_NAVIGATION_TEXT_FALLBACK = 'Forgot PIN'
ERROR_MESSAGE_TEXT_FALLBACK = 'Please enter a valid choice.\n'

# Custom quit screen
CUSTOM_QUIT_SCREEN_NAME_PREFIX = 'CustomErrorCommonQuitScreen'
CUSTOM_QUIT_SCREEN_NAME_CODE = '9999'
