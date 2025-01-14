import datetime
import types

class PromptLayerBase(object):
    __slots__ = ["_obj", "__weakref__", "_function_name", "_provider_type"]

    def __init__(self, obj, function_name="", provider_type="openai"):
        object.__setattr__(self, "_obj", obj)
        object.__setattr__(self, "_function_name", function_name)
        object.__setattr__(self, "_provider_type", provider_type)

    def __getattr__(self, name):
        return PromptLayerBase(
            getattr(object.__getattribute__(self, "_obj"), name),
            function_name=f'{object.__getattribute__(self, "_function_name")}.{name}',
            provider_type=object.__getattribute__(self, "_provider_type"),
        )

    def __delattr__(self, name):
        delattr(object.__getattribute__(self, "_obj"), name)

    def __setattr__(self, name, value):
        setattr(object.__getattribute__(self, "_obj"), name, value)

    def __call__(self, *args, **kwargs):
        from promptlayer.utils import get_api_key, promptlayer_api_request
        tags = kwargs.pop("pl_tags", None)
        request_start_time = datetime.datetime.now().timestamp()
        response = object.__getattribute__(self, "_obj")(*args, **kwargs)
        request_end_time = datetime.datetime.now().timestamp()
        if isinstance(response, types.GeneratorType):
            return response
        promptlayer_api_request(
            object.__getattribute__(self, "_function_name"),
            object.__getattribute__(self, "_provider_type"),
            args,
            kwargs,
            tags,
            response,
            request_start_time,
            request_end_time,
            get_api_key(),
        )
        return response
