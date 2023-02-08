from pathlib import Path

import docker
from git import Repo

from nymbus.config.envspec import EnvSpec
from nymbus.config.components.step import Step
from nymbus.tools.shell import Shell


def run(step: Step, env_spec: EnvSpec, component_path: Path, context: str):

    # Does it have a template?
    template = None
    if step.template:

        # Clone the repo if not existing
        tag = f"-b {step.template.tag}"
        repo_dir = component_path / ".nymbus" / "templates" / step.name / tag
        if not component_path.exists():
            Repo.clone_from(
                step.template.repository,
                repo_dir,
                multi_options=["--single-branch", f"-b {tag}"]
            )
        template = repo_dir

    # Does it have an associated image?
    if not step.image:
        run_locally(step, env_spec, component_path, context, template=template)
    else:
        run_in_docker(step, env_spec, component_path, context, template=template)


def run_locally(step: Step, env_spec: EnvSpec, component_path: Path, context: str, template: Path = None):
    # Run it locally
    Shell().run(
        step.command,
        cwd=context,
        env=env_spec.env
    )


def run_in_docker(step: Step, env_spec: EnvSpec, component_path: Path, context: str, template: Path = None):

    volumes = {
        str(component_path): {'bind': '/mnt/.nymbus/component', 'mode': 'rw'},
        context: {'bind': '/mnt/.nymbus/context', 'mode': 'ro'},
        **{path: dict(bind) for path, bind in step.image.volumes.items()},
    }
    volumes = volumes if not template else {**volumes, str(template): {'bind': '/mnt/.nymbus/template', 'mode': 'ro'}}

    # Run in Docker container
    client = docker.from_env()
    client.images.pull(step.image)
    client.containers.run(
        step.image.name,
        step.command,
        environment=env_spec.env,
        volumes=volumes,
        remove=True
    )


