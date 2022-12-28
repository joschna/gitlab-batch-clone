import yaml
import requests
import subprocess
from pathlib import Path
from typing import Iterable, List
from dataclasses import dataclass, field


CONFIG_FILE = 'gitlab.yaml'
TARGET_PATH = 'target'

@dataclass
class Project:
    path: str
    clone_url: str

@dataclass
class GitLab:
    host: str
    token: str
    groups: List[int] = field(default_factory=lambda:[])

    @staticmethod
    def from_configuration(filepath: str) -> 'GitLab':
        with open(filepath, 'r') as file:
            return GitLab(**yaml.safe_load(file))

    def get_projects(self) -> Iterable[Project]:
        for group in self.groups:
            url = f'https://{self.host}/api/v4/groups/{group}/projects?include_subgroups=true&pagination=keyset&per_page=20&order_by=id'
            while True:
                response = requests.get(url, headers = {'PRIVATE-TOKEN': self.token})

                for project in response.json():
                    yield Project(
                        project['path_with_namespace'],
                        f'{project["http_url_to_repo"][:8]}__token__:{self.token}@{project["http_url_to_repo"][8:]}')

                if next_page := response.links.get('next'):
                    url = next_page['url']
                else:
                    break


if __name__ == '__main__':

    target_path = Path(TARGET_PATH)

    if target_path.exists() and target_path.is_dir():
        print('Target directory already exists. Aborting ...')
        exit()

    target_path.mkdir()
    gitlab = GitLab.from_configuration(CONFIG_FILE)

    if input('Run concurrently in the background? [y/n]: ') == 'y':
        for project in gitlab.get_projects():
            subprocess.Popen(
                ['git', 'clone', project.clone_url, project.path],
                cwd=TARGET_PATH,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT)

        print('Started background processes to clone the repositories')

    else:
        for project in gitlab.get_projects():
            print('')
            subprocess.run(
                ['git', 'clone', project.clone_url, project.path],
                cwd=TARGET_PATH)

        print('\nDone')
