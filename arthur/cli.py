"""This module provides the Arthur CLI."""
# arthur/cli.py

from enum import StrEnum
from typing import Optional, Annotated

import subprocess
import typer
import os
import shutil


from arthur import __app_name__, __version__

app = typer.Typer()

class Framework(StrEnum):
    """The type of project to create."""

    express_ts = "express-ts"
    
    
def create_express_ts_project(yarn: bool):
    manager = "yarn" if yarn else "npm"
    install = "add" if yarn else "install"
    dev = "-D" if yarn else "--save-dev"
    
    typer.echo("Creating an Express TypeScript project...")
    subprocess.run([manager, "init", "-y"], shell=True)
    
    typer.echo("Installing dependencies...")
    subprocess.run([manager, install, "express"], shell=True)
    subprocess.run([manager, install, "cors"], shell=True)
    subprocess.run([manager, install, "winston"], shell=True)
    
    typer.echo("Installing dev dependencies...")
    subprocess.run([manager, install, dev, "typescript"], shell=True)
    subprocess.run([manager, install, dev, "@types/node"], shell=True)
    subprocess.run([manager, install, dev, "jest"], shell=True)
    subprocess.run([manager, install, dev, "@types/jest"], shell=True)
    subprocess.run([manager, install, dev, "ts-node"], shell=True)
    subprocess.run([manager, install, dev, "ts-jest"], shell=True)
    subprocess.run([manager, install, dev, "nodemon"], shell=True)
    subprocess.run([manager, install, dev, "@faker-js/faker"], shell=True)
    subprocess.run([manager, install, dev, "dotenv"], shell=True)
    
    typer.echo("Creating configuration files...")
    subprocess.run(["npx", "tsc", "--init"], shell=True)
    subprocess.run(["npx", "ts-jest", "config:init"], shell=True)


@app.command(name="new")
def new_project(
    framework: Annotated[Framework, typer.Option(help="Choose a framework for the project.")],
    name: Annotated[str, typer.Option(help="Give a name to the project.")],
    dockerfile: Annotated[bool, typer.Option(help="Create a standard Dockerfile for the project")] = False, # ! To be implemented
    yarn: Annotated[bool, typer.Option(help="Use Yarn as the package manager")] = False, # ! To be implemented
) -> None:
    """Create a new project. This command will create a folder with the project name and the necessary files for the chosen framework."""
    typer.echo("Creating a new project...")
    typer.echo(f"Framework: {framework}")
    typer.echo(f"Project name: {name}")
    
    typer.echo("Creating project folder...")
    path_on_system = os.getcwd()  
    dir_path  = os.path.join(path_on_system, name) 
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    os.chdir(dir_path)
    # subprocess.run(["mkdir", name])
    # subprocess.run(["cd", f'./{name}'])
    
    if framework == Framework.express_ts:
        create_express_ts_project(yarn)    


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
