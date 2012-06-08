from functools import partial
from urllib import urlencode

from flask import render_template, request
from jinja2 import Template

from . import app
from .data.graphite import graphs as graphite_graphs


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
                                    ['apache_report',
                                     'apache_server_report',
                                     'nginx_active_connections',
                                     'nginx_response_report',
                                     'nginx_server_report'],
                                   cluster='addons')
    graphs['Memcache'] = ganglia_graphs(default_reports + ['memcached_report'],
                                        cluster='Memcache AMO Cluster')
    graphs['Redis'] = ganglia_graphs(default_reports +
                                      ['amo_redis_prod_report'],
                                     cluster='amo-redis')

    return render_template('ganglia.html', graphs=graphs,
                            sizes=sizes, ranges=ranges, cur_size=cur_size,
                            cur_range=cur_range)


@app.route('/graphite')
def graphite():
    site = request.args.get('site', 'addons')
    graph = request.args.get('graph', 'all-responses')

    site_names = {
        'addons': 'Addons',
        'dev': 'Addons Dev',
        'stage': 'Addons Stage',
        'marketplace': 'Marketplace',
        'marketplace-dev': 'Marketplace Dev',
        'marketplace-stage': 'Marketplace Stage',
    }
    site_urls = {
        'addons': 'https://addons.mozilla.org',
        'dev': 'https://addons-dev.allizom.org',
        'stage': 'https://addons.allizom.org',
        'marketplace': 'https://marketplace.mozilla.org',
        'marketplace-dev': 'https://marketplace-dev.allizom.org',
        'marketplace-stage': 'https://marketplace.allizom.org',
    }
    sites = {
        'addons': 'addons',
        'dev': 'addons-dev',
        'stage': 'addons-stage',
        'marketplace': 'addons-marketplace',
        'marketplace-dev': 'addons-marketplacedev',
        'marketplace-stage': 'addons-marketplacestage',
    }

    data = {
        'base': '%s/render/?width=586&height=308' % app.config['GRAPHITE_BASE'],
        'site_url': site_urls[site],
        'site_urls': site_urls,
        'site_name': site_names[site],
        'site': sites[site],
        'updates': '&target=drawAsInfinite(stats.timers.%s.update.count)' % sites[site],
        'sites': sites,
        'fifteen': 'from=-15minutes&title=15 minutes',
        'hour': 'from=-1hours&title=1 hour',
        'day': 'from=-24hours&title=24 hours',
        'week': 'from=-7days&title=7 days',
        'month': 'from=-30days&title=30 days',
        'three_month': 'from=-90days&title=90 days',
        'ns': 'stats.%s' % sites[site]
    }
    graphs = {}
    for name, gs in graphite_graphs:
        slug = name.lower().replace(' ', '-')
        graphs[slug] = {
                'name': name, 'slug': slug,
                'url': [str(Template(g).render(data)) for g in gs],
                'updates': data['updates'],
        }

    data['graphs'] = sorted([(v['slug'], v['name'], v['url']) for v in graphs.values()])
    data['graph'] = graphs[graph]
    data['defaults'] = {'site': site, 'graph': graph}
    return render_template('graphite.html', **data)
