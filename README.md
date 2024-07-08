# grafana-synchronizer

## Intro

This code will help you to sync dashboards from Grafana -> Git

---

## How it works

In this version any dashboards with specific tag will be pushed to Git. Only one direction method. If you drop dashboard, which was copied to Git, it won't restore (due to one direction  pushing model).

All needed params are inside `config.py` file. Let's take a look what's inside:

```
# Grafana
grafana_url     - url of your grafana instance
grafana_api_key - Grafana token for Service Account
grafana_tag     - only dashboards with this tag will be pushed to Git

# GitLab
gitlab_repo_url - Gitlab URL (doesn't matter http/git url)
gitlab_branch   - destination Git branch
gitlab_token    - Git access token

# Common variables
local_repo_path - temporary local folder with git repo
```

