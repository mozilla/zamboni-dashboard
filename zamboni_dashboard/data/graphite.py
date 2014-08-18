graphs = (
    ['All Responses', ['vtitle=count&target=sumSeries({{ ns }}.response.*)&target={{ ns }}.response.200&target={{ ns }}.response.301&target={{ ns }}.response.302&target={{ ns }}.response.403&target={{ ns }}.response.404&target={{ ns }}.response.405&target={{ ns }}.response.500']],
    ['Site performance', ['vtitle=milleseconds&target=stats.timers.{{ site }}.view.GET.lower&target=stats.timers.{{ site }}.view.GET.mean&target=stats.timers.{{ site }}.view.GET.upper_90']],
    ['Redirects and Errors', ['vtitle=count&target={{ ns }}.response.301&target={{ ns }}.response.302&target={{ ns }}.response.304&target={{ ns }}.response.400&target={{ ns }}.response.403&target={{ ns }}.response.404&target={{ ns }}.response.405&target={{ ns }}.response.500&target={{ ns }}.response.503']],
    ['Celery', ['vtitle=count&target=sumSeries({{ site }}.celery.tasks.pending.*.*.*)&target=nonNegativeDerivative(sumSeries({{ site }}.celery.tasks.total.*.*.*))&target=nonNegativeDerivative(sumSeries({{ site }}.celery.tasks.failed.*.*.*))']],
    ['Validation', ['vtitle=unknown&target=stats.timers.{{ site }}.devhub.validator.lower&target=stats.timers.{{ site }}.devhub.validator.mean&target=stats.timers.{{ site }}.devhub.validator.upper_90']],
    ['GUID Search', ['vtitle=milleseconds&target=stats.timers.{{ site }}.view.api.views.guid_search.GET.lower&target=stats.timers.{{ site }}.view.api.views.guid_search.GET.mean&target=stats.timers.{{ site }}.view.api.views.guid_search.GET.upper_90&target=scale(stats.timers.{{ site }}.view.api.views.guid_search.GET.count(0.01)']],
    ['GUI Search Counts', ['vtitle=count&target=scale(stats.timers.{{ site }}.view.api.views.guid_search.GET.count,0.1)']],
    ['Update', ['vtitle=count&target=stats.timers.{{ site }}.services.update.lower&target=stats.timers.{{ site }}.services.update.mean&target=stats.timers.{{ site }}.services.update.upper_90&target=scale(stats.timers.{{ site }}.services.update.count(0.01)']],
    ['Verify', ['vtitle=count&target=stats.timers.{{ site }}.services.verify.lower&target=stats.timers.{{ site }}.services.verify.mean&target=stats.timers.{{ site }}.services.verify.upper_90&target=scale(stats.timers.{{ site }}.services.verify.count(0.01)']],
    ['Homepage', ['vtitle=count&target=stats.timers.{{ site }}.view.addons.views.home.GET.lower&target=stats.timers.{{ site }}.view.addons.views.home.GET.mean&target=stats.timers.{{ site }}.view.addons.views.home.GET.upper_90&target=scale(stats.timers.{{ site }}.view.addons.views.home.GET.count,0.1)']],
    ['Search', ['vtitle=count&target=stats.timers.{{ site }}.view.search.views.search.GET.lower&target=stats.timers.{{ site }}.search.raw.lower&target=stats.timers.{{ site }}.view.search.views.search.GET.mean&target=stats.timers.{{ site }}.search.raw.mean&target=stats.timers.{{ site }}.view.search.views.search.GET.upper_90&target=stats.timers.{{ site }}.search.raw.upper_90&target=scale(stats.timers.{{ site }}.view.search.views.search.GET.count,0.1)&target=scale(stats.timers.{{ site }}.search.raw.count,0.1)']],
    ['ES Request', ['vtitle=milleseconds'
                    '&target=stats.timers.{{ site }}.search.execute.lower'
                    '&target=stats.timers.{{ site }}.search.took.lower'
                    '&target=stats.timers.{{ site }}.search.execute.mean'
                    '&target=stats.timers.{{ site }}.search.took.mean'
                    '&target=stats.timers.{{ site }}.search.execute.upper_90'
                    '&target=stats.timers.{{ site }}.search.took.upper_90'
                    '&target=scale(stats.timers.{{ site }}.search.execute.count,0.1)'
                    '&target=scale(stats.timers.{{ site }}.search.took.count,0.1)']],
    ['Authenticated Responses', ['vtitle=milleseconds&target=stats.{{ site }}.response.auth.200&target=scale(stats.{{ site }}.response.200%2C0.1)&from=-1hours']],
    ['Marketplace', ['vtitle=count&target=stats.timers.{{ site }}.paypal.paykey.retrieval.upper_90']],
    ['Client', ['vtitle=unknown'
                '&target=stats.timers.{{ site }}.window.performance.timing.domInteractive.mean'
                '&target=stats.timers.{{ site }}.window.performance.timing.domInteractive.upper_90'
                '&target=stats.timers.{{ site }}.window.performance.timing.domComplete.mean'
                '&target=stats.timers.{{ site }}.window.performance.timing.domComplete.upper_90'
                '&target=stats.timers.{{ site }}.window.performance.timing.domLoading.mean'
                '&target=stats.timers.{{ site }}.window.performance.timing.domLoading.upper_90']],
    ['Client Counts', ['vtitle=count'
                '&target=stats.{{ site }}.window.performance.navigation.redirectCountstats'
                '&target=stats.{{ site }}.window.performance.navigation.type.back_forward'
                '&target=stats.{{ site }}.window.performance.navigation.type.navigate'
                '&target=stats.{{ site }}.window.performance.navigation.type.reload'
                '&target=stats.{{ site }}.window.performance.navigation.type.reserved']],
    ['Client Fragment', ['vtitle=count'
                '&target=stats.timers.{{ site }}.window.performance.timing.fragment.loaded.upper_90',
                '&target=stats.timers.{{ site }}.window.performance.timing.fragment.loaded.mean']],
    ['Error Counts', ['vtitle=count'
                      '&target=sumSeries(stats.{{ site }}.error.*)'
                      '&target=stats.{{ site }}.error.operationalerror']],
    ['Validator', ['vtitle=count&target={{ site }}.celery.tasks.total.devhub.tasks.validator'
                   '&target={{ site }}.celery.tasks.failed.devhub.tasks.validator'
                   '&target={{ site }}.celery.tasks.pending.devhub.tasks.validator']],
    ['Signing', ['vtitle=count&target=stats.timers.{{ site }}.services.sign.upper_90',
                 '&target=stats.timers.{{ site }}.services.sign.count']],
)

# List all the things.
_api_keys = [
    'abuse.api.AppAbuseViewSet',
    'abuse.api.UserAbuseViewSet',
    'account.views.AccountView',
    'account.views.FeedbackView',
    'account.views.InstalledView',
    'account.views.LoginView',
    'account.views.NewsletterView',
    'account.views.PermissionsView',
    'api.resources.CarrierViewSet',
    'api.resources.CategoryViewSet',
    'api.resources.ErrorViewSet',
    'api.resources.PriceCurrencyViewSet',
    'api.resources.PriceTierViewSet',
    'api.resources.RefreshManifestViewSet',
    'api.resources.RegionViewSet',
    'collections.views.CollectionImageViewSet',
    'collections.views.CollectionViewSet',
    'comm.api.CommViewSet',
    'comm.api.NoteViewSet',
    'comm.api.ReplyViewSet',
    'comm.api.ThreadViewSet',
    'developers.api.ContentRatingList',
    'developers.api.ContentRatingsPingback',
    'developers.api_payments.AddonPaymentAccountViewSet',
    'developers.api_payments.PaymentAccountViewSet',
    'developers.api_payments.PaymentAppViewSet',
    'developers.api_payments.PaymentCheckViewSet',
    'developers.api_payments.PaymentDebugViewSet',
    'developers.api_payments.PaymentViewSet',
    'developers.api_payments.UpsellViewSet',
    'features.views.AppFeaturesList',
    'fireplace.api.AppViewSet',
    'fireplace.api.FeaturedSearchView',
    'fireplace.api.SearchView',
    'monolith.resources.MonolithViewSet',
    'ratings.views.RatingFlagViewSet',
    'ratings.views.RatingViewSet',
    'reviewers.api.ApproveRegion',
    'reviewers.api.ReviewersSearchView',
    'reviewers.api.ReviewingView',
    'search.api.FeaturedSearchView',
    'search.api.SearchView',
    'search.api.SuggestionsView',
    'stats.api.AppStats',
    'stats.api.AppStatsTotal',
    'stats.api.GlobalStats',
    'stats.api.GlobalStatsTotal',
    'stats.api.TransactionAPI',
    'submit.api.PreviewViewSet',
    'submit.api.StatusViewSet',
    'submit.api.ValidationViewSet',
    'versions.api.VersionViewSet',
    'webapps.api.AppViewSet',
    'webapps.api.PrivacyPolicyViewSet',
    'webpay.resources.FailureNotificationView',
    'webpay.resources.PreparePayView',
    'webpay.resources.PricesViewSet',
    'webpay.resources.ProductIconViewSet',
    'webpay.resources.StatusPayView',
]

api = []
for key in _api_keys:
    target = ['vtitle=count']
    for verb in ['GET', 'POST', 'PATCH', 'PUT', 'DELETE']:
        target.append('target=stats.timers.{{ site }}.api.mkt.%s.%s.upper_90' % (key, verb))

    api.append([key, ['&'.join(target)]])


def _map(string, *args):
    data = []
    for x in args:
        data.append('target={0}.{1}'.format(string, x))
    return '&'.join(data)


webpay = [
    ['All Requests', [
        _map('stats.{{ site }}.response',
             '200', '301', '304', '400', '401', '404', '500'),
    ]],
    ['Timing', [
        _map('stats.timers.{{ site }}.view',
             'GET.mean', 'GET.mean_90', 'POST.mean', 'POST.mean_90')
    ]]
]


solitude = [
    ['All Requests', [
        _map('stats.{{ site }}.response',
             '200', '301', '304', '400', '401', '404', '500'),
    ]],
    ['Bango', [
        _map('stats.timers.{{ site }}.solitude.bango.request.*',
             'mean')
    ]],
    ['Boko', [
        _map('stats.timers.{{ site }}.solitude.boku.api',
             'count', 'mean', 'mean_90')
    ]]
]


solitude_proxy = [
   ['All Requests', [
        _map('stats.{{ site }}.response',
             '200', '301', '304', '400', '401', '404', '500'),
    ]],
    ['Bango', [
        _map('stats.timers.{{ site }}.solitude.proxy.bango.bango',
             'count', 'mean', 'mean_90')
    ]],
    ['Boku', [
        _map('stats.timers.{{ site }}.solitude.proxy.boku',
             'count', 'mean', 'mean_90')
    ]]
]
