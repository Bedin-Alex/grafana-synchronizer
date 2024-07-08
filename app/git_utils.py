import git
import os
import shutil
import logging
from config import gitlab_repo_url, gitlab_branch, gitlab_token, local_repo_path

logger = logging.getLogger(__name__)

def clone_or_pull_repo():
    if gitlab_repo_url.startswith('https://'):
        repo_url_with_token = gitlab_repo_url.replace('https://', f'https://oauth2:{gitlab_token}@')
    elif gitlab_repo_url.startswith('http://'):
        repo_url_with_token = gitlab_repo_url.replace('http://', f'http://oauth2:{gitlab_token}@')
    else:
        raise ValueError('Invalid URL scheme, should start with http:// or https://')

    try:
        if not os.path.exists(local_repo_path):
            logger.info(f'Cloning repository from {gitlab_repo_url} into {local_repo_path}')
            repo = git.Repo.clone_from(repo_url_with_token, local_repo_path, branch=gitlab_branch)
        else:
            repo = git.Repo(local_repo_path)
            origin = repo.remotes.origin
            origin.set_url(repo_url_with_token)
            logger.info(f'Pulling latest changes from {gitlab_branch} branch')
            origin.pull(gitlab_branch)
    except git.exc.InvalidGitRepositoryError:
        logger.warning(f'Invalid Git repository at {local_repo_path}, deleting and recloning')
        shutil.rmtree(local_repo_path)
        repo = git.Repo.clone_from(repo_url_with_token, local_repo_path, branch=gitlab_branch)
    except git.exc.GitCommandError as e:
        logger.error(f'Git command error: {e}')
        raise
    return repo

def commit_and_push_changes(repo):
    logger.info('Adding changes to git')
    repo.git.add(all=True)
    logger.info('Committing changes')
    repo.index.commit('Update dashboards from Grafana')
    logger.info(f'Pushing changes to {gitlab_branch} branch')
    repo.remotes.origin.push(gitlab_branch)
