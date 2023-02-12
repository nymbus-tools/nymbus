import logging
from pathlib import Path

import docker
from git import Repo

from nymbus.config.environment import NYMBUS_OUTPUT_FOLDER
from nymbus.config.envspec import EnvSpec
from nymbus.config.components.step import Step
from nymbus.tools.shell import Shell


logger = logging.getLogger(__name__)

DOCKER_CONTEXT = '/mnt/.nymbus/context'
DOCKER_OUTPUT = '/mnt/.nymbus/component'
DOCKER_TEMPLATE = '/mnt/.nymbus/template'


def run(step: Step, env_spec: EnvSpec, component_path: Path, context: str):

    # Touch the folder
    nymbus_folder = component_path / NYMBUS_OUTPUT_FOLDER
    nymbus_folder.mkdir(parents=True, exist_ok=True)

    # Does it have a template?
    template = None
    if step.template:

        # Clone the repo if not existing
        repo_dir = nymbus_folder / "templates" / step.name / step.template.tag
        if not repo_dir.exists():
            logger.info(f"Cloning {step.template.repository}...")
            Repo.clone_from(
                step.template.repository,
                repo_dir,
                branch=step.template.tag
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
        str(component_path/NYMBUS_OUTPUT_FOLDER): {'bind': '/mnt/.nymbus/component', 'mode': 'rw'},
        Path(context).absolute(): {'bind': '/mnt/.nymbus/context', 'mode': 'ro'},
        **{path: vars(bind) for path, bind in step.image.volumes.items()},
    }
    volumes = volumes if not template else {**volumes, str(template): {'bind': '/mnt/.nymbus/template', 'mode': 'ro'}}

    # Pull the image
    client = docker.from_env()
    logger.info(f"Pulling '{step.image.name}'...")
    client.images.pull(step.image.name)

    # Run in Docker container
    logger.info(f"Running '{step.command}'...")
    logger.info("-"*60)
    logs = client.containers.run(
        step.image.name,
        step.command if step.command else f"{DOCKER_TEMPLATE}/nymbus.sh",
        environment={
            **env_spec.env,
            "NYMBUS_CONTEXT": DOCKER_CONTEXT,
            "NYMBUS_OUTPUT": DOCKER_OUTPUT,
            "NYMBUS_TEMPLATE": DOCKER_TEMPLATE
        },
        volumes=volumes,
        remove=True,
        stderr=True,
        stream=True
    )
    for log in logs:
        logger.info(log.strip().decode())
    logger.info("-" * 60)

