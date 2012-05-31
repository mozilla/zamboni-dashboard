from functools import partial
from urllib import urlencode

from flask import render_template, request

from . import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ganglia')
def ganglia():

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

    ranges = ['hour', 'day', 'week', 'month', 'year']
    sizes = ['small', 'medium', 'large', 'xlarge']
    cur_range = request.args.get('range', 'hour')
    cur_size = request.args.get('size', 'medium')
    ganglia_graphs = partial(ganglia_graphs, r=cur_range, size=cur_size)

    default_reports = ['load_report', 'cpu_report',
                       'mem_report', 'network_report']
    graphs = {}
    graphs['Web'] = ganglia_graphs(default_reports +
                                    ['apache_report', 'apache_server_report'],
                                   cluster='addons')
    graphs['Memcache'] = ganglia_graphs(default_reports + ['memcached_report'],
                                        cluster='Memcache AMO Cluster')
    graphs['Redis'] = ganglia_graphs(default_reports +
                                      ['amo_redis_prod_report'],
                                     cluster='amo-redis')

    return render_template('ganglia.html', graphs=graphs,
                            sizes=sizes, ranges=ranges, cur_size=cur_size,
                            cur_range=cur_range)
