from fastapi import HTTPException


class ResponseObject(object):
    def __init__(self, _type, **kwargs):
        self.success = _type
        for k in kwargs.keys():
            self.__setattr__(k, kwargs[k])

    @classmethod
    def failure(cls, **kwargs):
        if "status_code" in kwargs:
            raise HTTPException(status_code=kwargs['status_code'], detail=kwargs['message'])
        return cls(False, **kwargs)

    @classmethod
    def success(cls, **kwargs):
        return cls(True, **kwargs)

    @classmethod
    def to_object(cls, **kwargs):
        return cls(**kwargs)
