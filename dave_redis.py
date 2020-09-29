import redis
import json


def get_session(host='localhost', strict=True):
    """
    Get a redis session.

    Parameters
    ----------
    host : str
        Name of redis host.
    strict : bool
        If True, it will return a "strict" session.

    Return
    ------
    redis session
    """
    if strict:
        connection_pool = redis.ConnectionPool(host=host, decode_responses=True)
        return redis.StrictRedis(connection_pool=connection_pool, charset='utf-8')
    return redis.Redis(host)


def get_all(rsession=None):
    """
    Get all redis keys into dictionary.

    Parameters
    ----------
    rsession : redis session or None
        If None, will start a new session.

    Return
    ------
    dict
    """
    if rsession is None:
        rsession = get_session()

    info = {}
    for key in rsession.keys():
        try:
            info[key] = rsession.get(key)
        except redis.ResponseError:
            info[key] = retrieve(key)
    return info


def retrieve(hash, rsession=None, show=False):
    """
    Retrieve a hash map.

    Parameters
    ----------
    hash : str
        Name of hash to return
    rsession : redis session or None
        If None, will start a new session.
    show : bool or str
        Show results.  If True, show all keys.  If str, just those keys.

    Return
    ------
    dict
    """
    if rsession is None:
        rsession = get_session()

    hred = rsession.hgetall(hash)  # could step through with hkeys then hget
    ret = {}
    for k, v in hred.items():
	try:
            ret[k] = json.loads(v)
        except ValueError:
            ret[k] = v
    if show:
        _qvu(ret, show)
    return ret


def insert(hash, hval, rsession=None):
    """
    Insert a dictionary into redis as a redis hash.

    Parameters
    hash : str
        Name of hash
    hval : dict
        Dictionary with data
    rsession : redis session or None
        If None, will start a new session.
    """
    if rsession is None:
        rsession = get_session()

    for k, v in hval.items():
        rsession.hset(hash, k, json.dumps(v))


def _qvu(adict, keys):
    """
    quick view
    """
    for k, v in adict.items():
        if keys is not None and k not in keys:
            continue
        print("{}:".format(k))
        if isinstance(v, str):
            prv = v[:40]
        elif isinstance(v, dict):
            prv = json.dumps(v, indent=2)
        else:
            prv = str(v)
        print("\t{}".format(prv))
