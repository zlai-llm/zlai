from functools import wraps
from warnings import warn
from typing import Any, Optional


__all__ = [
    "deprecated",
]


def deprecated(
        since: str,
        message: Optional[str] = None,
        name: Optional[str] = None,
        alternative: Optional[str] = None,
        pending: Optional[bool] = False,
        obj_type: Optional[str] = None,
        addendum: Optional[str] = None,
        removal: Optional[str] = None
) -> Any:
    """
    A decorator that can be used to mark functions, classes, or methods as deprecated.

    Parameters:
    since (str): The release at which this API became deprecated.
    message (str, optional): Override the default deprecation message. The %(since)s,
        %(name)s, %(alternative)s, %(obj_type)s, %(addendum)s, and %(removal)s format
        specifiers will be replaced by the values of the respective arguments passed
        to this function.
    name (str, optional): The name of the deprecated object.
    alternative (str, optional): An alternative API that the user may use in place of
        the deprecated API. The deprecation warning will tell the user about this
        alternative if provided.
    pending (bool, optional): If True, uses a PendingDeprecationWarning instead of a
        DeprecationWarning. Cannot be used together with removal.
    obj_type (str, optional): The object type being deprecated.
    addendum (str, optional): Additional text appended directly to the final message.
    removal (str, optional): The expected removal version. With the default (an empty
        string), a removal version is automatically computed from since. Set to other
        Falsy values to not schedule a removal date. Cannot be used together with pending.
    """
    def decorator(obj):
        message_template = message or "%(name)s is deprecated since %(since)s and will be removed in %(removal)s. Use %(alternative)s instead."

        @wraps(obj)
        def wrapper(*args, **kwargs):
            warn_type = PendingDeprecationWarning if pending else DeprecationWarning
            warn_msg = message_template % {
                'since': since,
                'name': name or getattr(obj, '__name__', 'this API'),
                'alternative': alternative or 'an alternative',
                'obj_type': obj_type or 'this',
                'addendum': f" {addendum}" if addendum else "",
                'removal': removal or f"version {float(since.split('.')[0]) + 1}"
            }
            warn(warn_msg, warn_type, stacklevel=2)
            return obj(*args, **kwargs)
        return wrapper
    return decorator
