from functools import partial
from urllib import urlencode

from flask import render_template, redirect, request
from jinja2 import Template

from . import app
from .data.graphite import (api as graphite_api_graphs,
                            webpay as graphite_webpay_graphs,
                            solitude as graphite_solitude_graphs,
                            solitude_proxy as graphite_solitude_proxy_graphs,
                            graphs as graphite_graphs)
from .data.nagios import get_nagios_service_status
from .data.pingdom import pingdom as pingdom_data
from .data.ganglia import ganglia_graphs
from default_settings import GRAPHITE_REST


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

    graphs = ganglia_graphs(cur_size, cur_range)

    return render_template('ganglia.html', graphs=graphs,
                            sizes=sizes, ranges=ranges, cur_size=cur_size,
                            cur_range=cur_range)


def get_graphite_data(site):
    return {
        'base': app.config['GRAPHITE_BASE'].get(site, GRAPHITE_REST) + '/render/?width=580&height=308',
        'site_name': app.config['GRAPHITE_SITE_NAMES'].get(site, site).replace('-', ' ').capitalize(),
        'site': app.config['GRAPHITE_SITES'].get(site, site),
        'updates': '&target=drawAsInfinite(stats.timers.%s.update.count)' % app.config['GRAPHITE_SITES'].get(site, site),
        'sites': sorted(app.config['GRAPHITE_SITES']),
        'fifteen': 'from=-15minutes&title=15 minutes',
        'hour': 'from=-1hours&title=1 hour',
        'day': 'from=-24hours&title=24 hours',
        'week': 'from=-7days&title=7 days',
        'month': 'from=-30days&title=30 days',
        'three_month': 'from=-90days&title=90 days',
        'ns': 'stats.%s' % app.config['GRAPHITE_SITES'].get(site, site)
    }


def get_template_data(source, data, graph, site):
    graphs = {}
    for name, gs in source:
        slug = name.lower().replace(' ', '-')
        partition = name.rpartition('.')
        graphs[slug] = {
            'name': name,
            'prefix': partition[0],
            'suffix': partition[2],
            'slug': slug,
            'url': [str(Template(g).render(data)) for g in gs],
            'updates': data['updates'],
        }
    data['graphs'] = graphs # sorted([(v['slug'], v['name'], v['url']) for v in graphs.values()])
    data['current_graph'] = graphs[graph]
    data['defaults'] = {'site': site, 'graph': graph}
    return data


@app.route('/graphite')
def graphite():
    site = request.args.get('site', app.config['GRAPHITE_DEFAULT_SITE'])
    graph = request.args.get('graph', 'all-responses')
    data = get_graphite_data(site)
    data['sites'] = {
        'dev': 'dev',
        'stage': 'stage',
        'addons': 'addons',
        'marketplace': 'marketplace',
        'marketplace-altdev': 'marketplace-altdev',
        'marketplace-dev': 'marketplace-dev',
        'marketplace-stage': 'marketplace-stage',
    }
    template_data = get_template_data(graphite_graphs, data, graph, site)
    return render_template('graphite.html', **template_data)


@app.route('/graphite-api')
def graphite_api():
    site = request.args.get('site', 'marketplace')
    graph = request.args.get('graph', 'fireplace.api.appviewset')
    data = get_graphite_data(site)
    data['sites'] = {
        'marketplace': 'marketplace',
        'marketplace-altdev': 'marketplace-altdev',
        'marketplace-dev': 'marketplace-dev',
        'marketplace-stage': 'marketplace-stage',
    }
    template_data = get_template_data(graphite_api_graphs, data, graph, site)
    # This only goes halfway across, we need a graphite update
    # for more. https://bugs.launchpad.net/graphite/+bug/1013308
    targets = (
        'threshold(500, "poor", orange)',
        'threshold(1000, "bad", red)',
        'drawAsInfinite(color(stats.timers.addons.update.count, "magenta"))'
    )
    template_data['thresholds'] = '&'.join('target=%s' % t for t in targets)
    return render_template('graphite.html', **template_data)


@app.route('/graphite/<server>/')
def graphite_server(server):
    servers = {
        'webpay': {
            'site': 'webpay',
            'sites': ['webpay', 'webpay-dev', 'webpay-stage',
                      'webpay-paymentsalt'],
            'graphs': graphite_webpay_graphs
        },
        'solitude': {
            'site': 'solitude',
            'sites': ['solitude', 'solitude-dev', 'solitude-stage',
                      'solitude-payments-alt'],
            'graphs': graphite_solitude_graphs
        },
        'proxy': {
            'site': 'solitude',
            'sites': ['solitude-proxy', 'solitude-proxy-dev',
                      'solitude-proxy-stage', 'solitude-proxy-payments-alt'],
            'graphs': graphite_solitude_proxy_graphs
        }
    }
    server = servers[server]
    site = request.args.get('site', server['site'])
    graph = request.args.get('graph', 'all-requests')
    data = get_graphite_data(site)
    data['sites'] = dict((s, s) for s in server['sites'])
    template_data = get_template_data(server['graphs'], data, graph, site)
    return render_template('graphite.html', **template_data)


@app.route('/nagios')
def nagios():
    status, updated = get_nagios_service_status()

    return render_template('nagios.html', status=status, updated=updated)


@app.route('/pingdom')
def pingdom():
    checks = pingdom_data.checks(with_summary=True)
    checks.sort(key=lambda x: x['name'])
    return render_template('pingdom.html', checks=checks)
