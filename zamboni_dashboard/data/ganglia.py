from .. import app
from urllib import urlencode

def ganglia_graphs(size='small', r='hour'):
    graphs = {}
    for group, base_url, cluster, monitors in app.config['GANGLIA_GROUPS']:
        monitors = monitors + app.config['GANGLIA_DEFAULT_REPORTS']
        graphs[group] = [ganglia_graph(m, base_url, cluster, size, r) for m in monitors]
    return graphs

def ganglia_graph(name, base_url, cluster, size='medium',
                        r='hour', t='g', host=None):
    query = {'c': cluster,
             'z': size,
             'r': r,
             t: name}
    if host:
        query['host'] = host

    return "%s/graph.php?%s" % (base_url,
                                urlencode(query))
