from .. import app
from urllib import urlencode

def ganglia_graphs(names, *args, **kwargs):
    return [ganglia_graph(n, *args, **kwargs) for n in names]

def ganglia_graph(name, cluster, size='medium',
                        r='hour', t='g', host=None):
    query = {'c': cluster,
             'z': size,
             'r': r,
             t: name}
    if host:
        query['host'] = host

    return "%s/graph.php?%s" % (app.config['GANGLIA_BASE'],
                                urlencode(query))
