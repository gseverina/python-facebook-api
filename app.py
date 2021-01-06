import requests
from json import dumps
from yaml import load, FullLoader

ENV = {
    'APP_ID': '',
    'APP_SECRET': '',
    'ACCESS_TOKEN': '',
    'ACCOUNT': '',
    'USER_ID': ''
}
URL = "https://graph.facebook.com/v9.0/"
EDGES = {
    'adaccounts': {},
    #    '': {},
    #    'feed': {},
    #    'photos': {},
    #    'posts': {},
    #    'accounts': {},
    #    'assigned_ad_accounts': {}
}
TIME_RANGE = '{"since":"2020-09-01","until":"2020-11-01"}'
BREAKDOWNS = 'age,gender'
ADACCOUNTS = {}


def __load_credentials(cred_file='fb_creds.yml'):
    with open(cred_file) as file:
        credentials = load(file, Loader=FullLoader)
        ENV['APP_ID'] = credentials['appid']
        ENV['APP_SECRET'] = credentials['appsecret']
        ENV['ACCESS_TOKEN'] = credentials['accesstoken']
        ENV['ACCOUNT'] = credentials['sysuser']
        ENV['USER_ID'] = credentials['sysuser'][4:]


def __get_node_data(node_id, edge=''):
    params = (
        ('access_token', ENV['ACCESS_TOKEN']),
    )

    resp = requests.get(f'{URL}{node_id}/{edge}', params=params)
    return resp.json()


def load_edges_data():
    for edge in EDGES.keys():
        EDGES[edge] = __get_node_data(ENV['USER_ID'], edge)


def __get_campaigns(acc_id):
    params = (
        ('time_range', TIME_RANGE),
        ('access_token', ENV['ACCESS_TOKEN']),
    )
    resp = requests.get(f'{URL}{acc_id}/campaigns', params=params)
    return resp.json()


def __get_insights(acc_id):
    params = (
        ('breakdowns', BREAKDOWNS),
        ('fields', 'impressions,reach'),
        ('time_range', TIME_RANGE),
        ('access_token', ENV['ACCESS_TOKEN']),
    )
    resp = requests.get(f'{URL}{acc_id}/insights', params=params)
    return resp.json()


def __accumulate_insights(insights_data):
    for d in insights_data:
        key = d['age'] + '-' + d['gender']
        if key in ADACCOUNTS.keys():
            i, r = int(d['impressions']), int(d['reach'])
            ADACCOUNTS[key]['impressions'] += i
            ADACCOUNTS[key]['reach'] += r
        else:
            ADACCOUNTS[key] = {
                'impressions': int(d['impressions']),
                'reach': int(d['reach'])
            }


def load_campaigns_data():
    for item in EDGES['adaccounts']['data']:
        ad_account_id = item['id']

        campaigns = __get_campaigns(ad_account_id)
        if len(campaigns['data']) > 0:
            for camp in campaigns['data']:
                camp_id = camp['id']
                insights = __get_insights(camp_id)
                __accumulate_insights(insights['data'])


def load_adaccounts_data():
    # for each ad account...
    for item in EDGES['adaccounts']['data']:
        ad_account_id = item['id']

        # get insight data...
        insights = __get_insights(ad_account_id)

        # sum impressions and reach grouped by age and gender...
        __accumulate_insights(insights['data'])


def handler(event, context):
    __load_credentials()
    load_edges_data()
    load_adaccounts_data()

    return {
        'statusCode': 200,
        'body': dumps(ADACCOUNTS)
    }
