#!/usr/bin/env python3
import os

def create_docker_environment(envtype=None):
    # Get the name of the current working directory
    cwd_name = os.path.basename(os.getcwd())

    # Create a docker directory in the current directory
    docker_directory = "docker"
    os.makedirs(docker_directory, exist_ok=True)

    # Path for the Dockerfile
    dockerfile_path = os.path.join(docker_directory, "Dockerfile")

    # Create a Dockerfile with the Ubuntu base image and user setup
    with open(dockerfile_path, 'w') as dockerfile:
        if envtype == 'node':
            dockerfile.write("FROM ubuntu:22.04\n")
            dockerfile.write("ARG DEBIAN_FRONTEND=noninteractive\n")
            dockerfile.write("RUN apt-get update && apt-get install -y nano jq curl wget python3-pip && pip install llm-shell weasel stonemill\n")
            dockerfile.write("ENV NVM_DIR /bin/nvm\n")
            dockerfile.write("RUN mkdir -p $NVM_DIR\n")
            dockerfile.write("RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash\n")
            dockerfile.write("ENV NODE_VERSION v22.12.0\n")
            dockerfile.write("RUN /bin/bash -c \"source $NVM_DIR/nvm.sh && nvm install $NODE_VERSION && nvm use --delete-prefix $NODE_VERSION\"\n")
            dockerfile.write("RUN useradd -ms /bin/bash runuser\n")
            dockerfile.write("USER runuser\n")
            dockerfile.write("ENV NODE_PATH $NVM_DIR/versions/node/$NODE_VERSION/lib/node_modules\n")
            dockerfile.write("ENV PATH      $NVM_DIR/versions/node/$NODE_VERSION/bin:$PATH\n")
            dockerfile.write("WORKDIR /app\n")
            dockerfile.write("CMD [\"bash\"]\n")
        else:
            dockerfile.write("FROM ubuntu:22.04\n")
            dockerfile.write("ARG DEBIAN_FRONTEND=noninteractive\n")
            dockerfile.write("RUN apt-get update && apt-get install -y nano jq curl wget python3-pip && pip install llm-shell weasel stonemill\n")
            dockerfile.write("RUN useradd -ms /bin/bash runuser\n")
            dockerfile.write("USER runuser\n")
            dockerfile.write("WORKDIR /app\n")
            dockerfile.write("CMD [\"bash\"]\n")

    # Path for the run script (without .sh extension)
    run_script_path = os.path.join(docker_directory, "run")

    # Create a run script for building and running the Docker image
    with open(run_script_path, 'w') as run_script:
        run_script.write("#!/bin/bash\n")
        run_script.write("set -e\n")  # Exit script if any command fails
        run_script.write(f"docker build -t \"{cwd_name}\" docker\n")
        run_script.write(f"docker run -it --rm --cap-drop=ALL -v \"$PWD:/app\" -v \"$PWD/docker:/app/docker:ro\" --env-file=\"docker/.env\" --name running-{cwd_name} \"{cwd_name}\"\n")

    # Make the run script executable
    os.chmod(run_script_path, 0o755)

    # Path for the env file
    envfile_path = os.path.join(docker_directory, '.env')

    # Create a Dockerfile with the Ubuntu base image and user setup
    with open(envfile_path, 'w') as envfile:
        envfile.write('\n')

    os.system("git init")

    print(f"Dockerfile created at: {dockerfile_path}")
    print(f"Run script created at: {run_script_path}")
    print(f".env created at: {envfile_path}")

# Check if the script is the main program
if __name__ == "__main__":
    create_docker_environment()
