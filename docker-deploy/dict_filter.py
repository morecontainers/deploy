def dict_filter(adict, blacklist=(), *, path=None):
    if not isinstance(blacklist, (list, set, tuple)):
        raise TypeError("must be list, set or tuple")
    if isinstance(adict, dict):
        adict = {
            key: dict_filter(
                value, blacklist=blacklist, path=(path + "." + key if path else key),
            )
            for key, value in adict.items()
            if (path + "." + key if path else key) not in blacklist
        }
    return adict
