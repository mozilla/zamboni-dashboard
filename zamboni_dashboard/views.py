from functools import partial
from urllib import urlencode

from flask import render_template, redirect, request
from jinja2 import Template

from . import app
from .data.graphite import graphs as graphite_graphs
from .data.nagios import get_nagios_service_status
from .data.pingdom import pingdom as pingdom_data
from .data.ganglia import ganglia_graphs



@app.route('/')
def index():
    status, updated = get_nagios_service_status()
    all_services = {'all': [], 'OK': [],
                    'WARNING': [], 'CRITICAL': [], 'UNKNOWN': []}

    for group, group_status in status:
        for service_type, levels in group_status.iteritems():
            for level, services in levels.iteritems():
                all_services[level].extend(services)

    return render_template('index.html', services=all_services, updated=updated)


@app.route('/ganglia')
def ganglia():

    ranges = ['hour', 'day', 'week', 'month', 'year']
    sizes = ['small', 'medium', 'large', 'xlarge']
    cur_range = request.args.get('range', 'hour')
    cur_size = request.args.get('size', 'small')
    # putting ganglia_graphs in a lib causes a problem here when trying to reuse the name,
    # so we call it ganglia_graphs_sized locally
    ganglia_graphs_sized = partial(ganglia_graphs, r=cur_range, size=cur_size)

    graphs = {}
    graphs['Web'] = ganglia_graphs_sized(app.config['GANGLIA_DEFAULT_REPORTS'] +
                                    ['apache_report',
                                     'apache_server_report',
                                     'nginx_active_connections',
                                     'nginx_response_report',
                                     'nginx_server_report'],
                                   cluster='addons')
    graphs['Memcache'] = ganglia_graphs_sized(app.config['GANGLIA_DEFAULT_REPORTS'] + ['memcached_report'],
                                        cluster='Memcache AMO Cluster')
    graphs['Redis'] = ganglia_graphs_sized(app.config['GANGLIA_DEFAULT_REPORTS'] +
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
        'base': '%s/render/?width=580&height=308' % app.config['GRAPHITE_BASE'],
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


@app.route('/nagios')
def nagios():
    status, updated = get_nagios_service_status()

    return render_template('nagios.html', status=status, updated=updated)


@app.route('/pingdom')
def pingdom():
    checks = pingdom_data.checks(with_summary=True)
    checks.sort(key=lambda x: x['name'])
    return render_template('pingdom.html', checks=checks)
