from . import loader
from .registry import registry
from .states.base import ImageState


class Image(object):
    def __init__(self, initial_state):
        self.state = initial_state

    def __getattr__(self, attr):
        new_state = None

        try:
            operation = registry.get_operation(type(self.state), attr)
        except LookupError:
            try:
                new_state = registry.find_state(with_converter_from=type(self.state), with_operation=attr)
                operation = registry.get_operation(new_state, attr)
            except LookupError:
                raise AttributeError("%r object has no attribute %r" % (
                    self.__class__.__name__, attr
                ))

        def wrapper(*args, **kwargs):
            if new_state:
                converter = registry.get_converter(type(self.state), new_state)
                self.state = converter(self.state)

            return_value = operation(self.state, *args, **kwargs)

            if isinstance(return_value, ImageState):
                self.state = return_value

            return return_value

        return wrapper

    # A couple of helpful methods

    @classmethod
    def open(cls, f):
        return cls(loader.load_image(f))

    def save(self, image_format, output):
        # Get operation name
        operation_name = 'save_as_' + image_format
        return getattr(self, operation_name)(output)
