"""
Generate configuration files into generated_dir.
"""
from fabric.api import abort, env, task

from confab.conffiles import iterconffiles
from confab.output import status
from confab.validate import validate_generate


@task
def generate(templates_dir=None,
             data_dir=None,
             generated_dir=None):
    """
    Generate configuration files.
    """
    validate_generate(templates_dir, data_dir, generated_dir)

    if not env.confab:
        abort("Confab needs to be configured")

    for conffiles in iterconffiles(env.confab, templates_dir, data_dir):
        status("Generating templates for '{environment}' and '{role}'",
               environment=env.confab.name,
               role=conffiles.role)

        conffiles.generate(generated_dir)
