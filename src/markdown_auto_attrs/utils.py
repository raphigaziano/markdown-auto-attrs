"""
Helpers function.

"""
import sys
from importlib import import_module

# dynamic imports (lifted from django:
# https://github.com/django/django/blob/main/django/utils/module_loading.py)


def cached_import(module_path, class_name):
    # Check whether module is loaded and fully initialized.
    if not (
        (module := sys.modules.get(module_path))
        and (spec := getattr(module, "__spec__", None))
        and getattr(spec, "_initializing", False) is False
    ):
        module = import_module(module_path)
    return getattr(module, class_name)


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    try:
        return cached_import(module_path, class_name)
    except AttributeError as err:
        raise ImportError(
            'Module "%s" does not define a "%s" attribute/class'
            % (module_path, class_name)
        ) from err


# callback handling

def get_callback(cb):
    """
    Return `cb` directly if its a callable. Try and import it if it's a string.
    Return None otherwise.
    """
    if callable(cb):
        return cb
    elif isinstance(cb, str):
        return import_string(cb)
    return None
