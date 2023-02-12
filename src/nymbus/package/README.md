# Nymbus
Deploy any code anywhere

## Usage

### Run

You can run 

```
nymbus run [--step STEP] <component> <env>
```

To execute the steps specified in `./<component>/<env>.nymbus.yml`

### Folder and file structure

Complete example in https://github.com/nymbus-tools/nymbus/src/nymbus/tests/data/simple_project

Each folder **MUST** have a `default.nymbus.yml` to be explored (even the root one of your components).

Nymbus files will be merged (first `default.nymbus.yml`, then `<env>.nymbus.yml`)

```
# Optional: environment variables for all the steps
env:
  PROJECT: project-dev
  SECRET: ${DEV_SECRET}  # This will be taken at runtime

# Optional: path to context, i.e. folder that will be visible to command
context: ../../

# Step definitions
steps:

  # Name of step
  build:
    env:
      STANDARD: low
      CLOUDSDK_CONFIG: /gcloud
      
    # Command to execute
    # (if not specified and image is specified, will be /mnt/.nymbus/template/nymbus.sh)
    command: ls -la /mnt/.nymbus/template
    
    # Optional: an image where to run the command
    # !!!MUST HAVE DOCKER INSTALLED!!!
    image: 
      name: google/cloud-sdk:159.0.0
      # Optional extra volumes to mount
      volumes:
        ~/AppData/Roaming/gcloud:
            bind: /gcloud
            mode: ro
    
    # Optional: a git repo containing scripts to run
    # mounted in /mnt/.nymbus/template
    # !!!MUST HAVE GIT INSTALLED!!!
    # !!!WORKING JUST IN CASE OF DOCKER!!!
    template:
      repository: git@github.com:nymbus-tools/nymbus.git  # or https://
      tag: feat/init  # or branch (default: master)
    
  # Name of step
  other:
    command: echo ok
```
