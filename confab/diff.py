"""
Determine the difference between remote and generated configuration files.
"""
from fabric.api import abort, env, task

from confab.conffiles import iterconffiles
from confab.output import status
from confab.validate import validate_all


@task
def diff(templates_dir=None,
         data_dir=None,
         generated_dir=None,
         remotes_dir=None):
    """
    Show configuration file diffs.
    """
    validate_all(templates_dir, data_dir, generated_dir, remotes_dir)

    if not env.confab:
        abort("Confab needs to be configured")

    for conffiles in iterconffiles(env.confab, templates_dir, data_dir):
        status("Computing template diffs for '{environment}' and '{role}'",
               environment=env.confab.name,
               role=conffiles.role)

        conffiles.diff(generated_dir, remotes_dir)
