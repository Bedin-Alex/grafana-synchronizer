import logging
import os
import json

from git_utils import clone_or_pull_repo, commit_and_push_changes, local_repo_path
from grafana_utils import get_dashboards_by_tag, get_dashboard_json, sanitize_filename
from config import grafana_tag

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def update_repo_with_dashboards(repo, dashboards):
    dashboards_path = os.path.join(local_repo_path, 'dashboards')
    os.makedirs(dashboards_path, exist_ok=True)

    for dashboard in dashboards:
        dashboard_json = get_dashboard_json(dashboard['uid'])
        dashboard_title = dashboard_json['title']
        dashboard_folder = dashboard_json.get('folderTitle', 'general')
        dashboard_filename = sanitize_filename(dashboard_title) + ".json"
        folder_path = os.path.join(dashboards_path, sanitize_filename(dashboard_folder))
        os.makedirs(folder_path, exist_ok=True)
        dashboard_filepath = os.path.join(folder_path, dashboard_filename)
        
        if os.path.exists(dashboard_filepath):
            with open(dashboard_filepath, 'r') as f:
                existing_dashboard = json.load(f)
            if existing_dashboard == dashboard_json:
                logger.info(f'No changes in dashboard: {dashboard_title} (UID: {dashboard["uid"]})')
                continue
        
        logger.info(f'Updating dashboard: {dashboard_title} (UID: {dashboard["uid"]}) in folder: {dashboard_folder}')
        with open(dashboard_filepath, 'w') as f:
            json.dump(dashboard_json, f, indent=4)

    commit_and_push_changes(repo)

def main():
    logger.info('Starting synchronization process')
    dashboards = get_dashboards_by_tag(grafana_tag)

    repo = clone_or_pull_repo()
    update_repo_with_dashboards(repo, dashboards)
    logger.info('Synchronization process completed')

if __name__ == '__main__':
    main()
