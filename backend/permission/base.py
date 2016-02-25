class PermissionBase:
    @classmethod
    def check(cls, req, data):
        return cls.__getattribute__(cls, req.request.method.lower())(req, data)
