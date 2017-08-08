from functools import wraps

def cache(getter):
    """Given a property-getter style function, return a new function
    that lazily caches the result of this in the object.
    """
    name = '_' + getter.__name__
    @wraps(getter)
    def wrapper(self):
        try:
            return getattr(self, name)
        except AttributeError:
            ans = getter(self)
            setattr(self, name, ans)
            return ans
    return wrapper
