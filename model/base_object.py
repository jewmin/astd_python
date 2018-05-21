# -*- coding: utf-8 -*-
# 对象基类


class BaseObject(object):
    def __init__(self):
        super(BaseObject, self).__init__()

    def handle_info(self, dict_info):
        for key, value in dict_info.iteritems():
            if hasattr(self, key):
                origin = getattr(self, key)
                if isinstance(origin, BaseObject):
                    origin.handle_info(value)
                elif isinstance(origin, int):
                    setattr(self, key, int(value))
                elif isinstance(origin, float):
                    setattr(self, key, float(value))
                else:
                    setattr(self, key, value)
