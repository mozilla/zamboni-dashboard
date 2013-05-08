from functools import partial
from urllib import urlencode

from flask import render_template, redirect, request
from jinja2 import Template

from . import app
from .data.graphite import (api as graphite_api_graphs,
                            graphs as graphite_graphs)
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

    graphs = ganglia_graphs(cur_size, cur_range)

    return render_template('ganglia.html', graphs=graphs,
                            sizes=sizes, ranges=ranges, cur_size=cur_size,
                            cur_range=cur_range)


def get_graphite_data(site):
    return {
        'base': '%s/render/?width=580&height=308' % app.config['GRAPHITE_BASE'],
        'site_url': app.config['GRAPHITE_SITE_URLS'][site],
        'site_urls': app.config['GRAPHITE_SITE_URLS'],
        'site_name': app.config['GRAPHITE_SITE_NAMES'][site],
        'site': app.config['GRAPHITE_SITES'][site],
        'updates': '&target=drawAsInfinite(stats.timers.%s.update.count)' % app.config['GRAPHITE_SITES'][site],
        'sites': app.config['GRAPHITE_SITES'],
        'fifteen': 'from=-15minutes&title=15 minutes',
        'hour': 'from=-1hours&title=1 hour',
        'day': 'from=-24hours&title=24 hours',
        'week': 'from=-7days&title=7 days',
        'month': 'from=-30days&title=30 days',
        'three_month': 'from=-90days&title=90 days',
        'ns': 'stats.%s' % app.config['GRAPHITE_SITES'][site]
    }

def get_template_data(source, data, graph, site):
    graphs = {}
    for name, gs in source:
        slug = name.lower().replace(' ', '-')
        graphs[slug] = {
            'name': name, 'slug': slug,
            'url': [str(Template(g).render(data)) for g in gs],
            'updates': data['updates'],
        }

    data['graphs'] = sorted([(v['slug'], v['name'], v['url']) for v in graphs.values()])
    data['graph'] = graphs[graph]
    data['defaults'] = {'site': site, 'graph': graph}
    return data


@app.route('/graphite')
def graphite():
    site = request.args.get('site', app.config['GRAPHITE_DEFAULT_SITE'])
    graph = request.args.get('graph', 'all-responses')
    data = get_graphite_data(site)
    template_data = get_template_data(graphite_graphs, data, graph, site)
    return render_template('graphite.html', **template_data)


@app.route('/graphite-api')
def graphite_api():
    site = request.args.get('site', 'marketplace')
    graph = request.args.get('graph', 'apps')
    data = get_graphite_data(site)
    data['sites'] = {
        'marketplace': 'marketplace',
        'marketplace-altdev': 'marketplace-altdev',
        'marketplace-dev': 'marketplace-dev',
        'marketplace-stage': 'marketplace-stage',
    }
    template_data = get_template_data(graphite_api_graphs, data, graph, site)
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
