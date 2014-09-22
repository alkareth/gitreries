# -*-coding:Utf-8 -*

def cache(_cache={}, *args):
    if args[:-1] not in _cache:
        _cache[args[:-1]] = args[-1]
        print("{} mis en cache".format(args[-1]))
    return _cache[args[:-1]]
