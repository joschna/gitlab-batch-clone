# GitLab Batch Clone

Clone a list of repositories based on GitLab groups.

## Usage

The script requires a `gitlab.yaml` file which follows the schema

```yaml
host: gitlab.com
token: <gitlab-token> # with read_api and read_repository permissions
groups:
  - 1111 # Group 1
  - 2222 # Group 2
  - ...
```

Prepare the requirements by running `python -m pip install -r requirements.txt`.

It offers two cloning modes: syncronous and asyncronous. The latter is rather experimental and will consume a lot of resources (and most probably block your system for a while), but run a lot faster in general. You will be prompted for your choice while running the script with `python main.py`.
