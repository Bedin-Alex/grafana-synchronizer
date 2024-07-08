import requests
import logging
import re
from config import grafana_url, grafana_api_key

logger = logging.getLogger(__name__)

def get_dashboards_by_tag(tag):
    headers = {
        'Authorization': f'Bearer {grafana_api_key}',
        'Content-Type': 'application/json'
    }
    logger.info(f'Fetching dashboards with tag: {tag}')
    response = requests.get(f'{grafana_url}/api/search?tag={tag}', headers=headers)
    response.raise_for_status()
    dashboards = response.json()
    logger.info(f'Found {len(dashboards)} dashboards')
    return dashboards

def get_dashboard_json(dashboard_uid):
    headers = {
        'Authorization': f'Bearer {grafana_api_key}',
        'Content-Type': 'application/json'
    }
    logger.info(f'Fetching JSON for dashboard UID: {dashboard_uid}')
    response = requests.get(f'{grafana_url}/api/dashboards/uid/{dashboard_uid}', headers=headers)
    response.raise_for_status()
    dashboard = response.json()['dashboard']
    return dashboard

def sanitize_filename(name):
    """Drop not needed characters"""
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', name)
