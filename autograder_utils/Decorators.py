import base64
import os.path
from functools import wraps


class Weight(object):
    """Simple decorator to add a __weight__ property to a function

    Usage: @weight(3.0)
    """

    def __init__(self, val):
        self.val = val

    def __call__(self, func):
        func.__weight__ = self.val
        return func


class Number(object):
    """Simple decorator to add a __number__ property to a function

    Usage: @number("1.1")

    This field will then be used to sort the test results on Gradescope.
    """

    def __init__(self, val):
        self.val = str(val)

    def __call__(self, func):
        func.__number__ = self.val
        return func


class Visibility(object):
    """Simple decorator to add a __visibility__ property to a function

    Usage: @visibility("hidden")

    Options for the visibility field are as follows:

    - `hidden`: test case will never be shown to students
    - `after_due_date`: test case will be shown after the assignment's due date has passed.
      If late submission is allowed, then test will be shown only after the late due date.
    - `after_published`: test case will be shown only when the assignment is explicitly published from the "Review Grades" page
    - `visible` (default): test case will always be shown
    """

    def __init__(self, val):
        self.val = val

    def __call__(self, func):
        func.__visibility__ = self.val
        return func


class HideErrors(object):
    """Simple decorator to add a __hide_errors__ property to a function

    Usage: @hide_errors("Error message to be shown upon test failure")

    Used to hide the particular source of an error which caused a test to fail.
    Otherwise, a test's particular assertions can be seen by students.
    """

    def __init__(self, val="Test failed"):
        self.val = val

    def __call__(self, func):
        func.__hide_errors__ = self.val
        return func


class Tags(object):
    """Simple decorator to add a __tags__ property to a function

    Usage: @tags("concept1", "concept2")
    """

    def __init__(self, *args):
        self.tags = args

    def __call__(self, func):
        func.__tags__ = self.tags
        return func


class Leaderboard(object):
    """Decorator that indicates that a test corresponds to a leaderboard column

    Usage: @leaderboard("high_score"). The string parameter indicates
    the name of the column on the leaderboard

    Then, within the test, set the value by calling
    kwargs['set_leaderboard_value'] with a value. You can make this convenient by
    explicitly declaring a set_leaderboard_value keyword argument, eg.

    ```
    def test_highscore(set_leaderboard_value=None):
        set_leaderboard_value(42)
    ```

    """

    def __init__(self, column_name, sort_order='desc'):
        self.column_name = column_name
        self.sort_order = sort_order

    def __call__(self, func):
        func.__leaderboard_column__ = self.column_name
        func.__leaderboard_sort_order__ = self.sort_order

        def set_leaderboard_value(x):
            wrapper.__leaderboard_value__ = x

        @wraps(func)
        def wrapper(*args, **kwargs):
            kwargs['set_leaderboard_value'] = set_leaderboard_value
            return func(*args, **kwargs)

        return wrapper


class ImageResult:
    """
    Decorator that allows the setting of image data to be rendered in the test results

    Usage: @ImageResult

    Then, within the test, make sure the final two parameters are ``encode_image_data`` and ``set_image_data``.

    ``encode_image_data`` takes an *absolute* path to the image to load and returns the base-64 encoded version of that image.

    ``set_image_data`` takes the label for the image, the actual data for the image, and the image type (default is png) and sets it within the result for further processing
    """

    def __init__(self):
        pass

    def __call__(self, func):
        def encode_image_data(image_bytes):
            image_encoded_bytes = base64.b64encode(image_bytes)

            return image_encoded_bytes.decode("utf-8")

        def set_image_data(label, data, image_type="png"):
            wrapper.__image_data__ = {
                'label': label,
                'data': data,
                'image_type': image_type,
            }

        @wraps(func)
        def wrapper(*args, **kwargs):
            mut_args = list(*args) if len(args) != 1 else [args[0]]
            mut_args.extend([encode_image_data, set_image_data])

            return func(*tuple(mut_args), **kwargs)

        return wrapper


class PartialCredit(object):
    """Decorator that indicates that a test allows partial credit

    Usage: @partial_credit(test_weight)

    Then, within the test, set the value by calling
    kwargs['set_score'] with a value. You can make this convenient by
    explicitly declaring a set_score keyword argument, eg.

    ```
    @partial_credit(10)
    def test_partial(set_score=None):
        set_score(4.2)
    ```

    """

    def __init__(self, weight):
        self.weight = weight

    def __call__(self, func):
        func.__weight__ = self.weight

        def set_score(x):
            wrapper.__score__ = x

        @wraps(func)
        def wrapper(*args, **kwargs):
            kwargs['set_score'] = set_score
            return func(*args, **kwargs)

        return wrapper
