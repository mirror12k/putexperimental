#!/usr/bin/env python3
import os
from pathlib import Path
import sys
import re
from putdockerfile import create_docker_environment

def create_experimental_directory(experiment_name, envtype=None):
    if not re.match(r"^[a-zA-Z0-9\-_]+$", experiment_name):
        raise Exception('invalid experiment_name: ' + experiment_name)

    experiments_directory = Path.home() / "src" / "experimental"
    new_experimental_directory = os.path.join(experiments_directory, experiment_name)
    os.makedirs(new_experimental_directory)

    os.chdir(new_experimental_directory)
    create_docker_environment(envtype)
    print(f"Experimental directory created at: {new_experimental_directory}")
    print(f"Make sure to execute: cd {new_experimental_directory}")

# Check if the script is the main program
if __name__ == "__main__":
    if len(sys.argv) > 2:
        create_experimental_directory(sys.argv[1], sys.argv[2])
    else:
        create_experimental_directory(sys.argv[1], None)
