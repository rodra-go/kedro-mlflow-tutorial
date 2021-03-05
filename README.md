# Kedro MLFlow Tutorial

This tutorial objective is to apply engineering best practices in machine learning development and experimentation using the [Kedro](https://kedro.readthedocs.io/en/stable/) framework along with a [Kedro's plugin](https://kedro-mlflow.readthedocs.io/en/stable/) for [MLFlow](https://mlflow.org/docs/latest/index.html). The information in this README file is limited, as the tutorial video is available [here](). So if the information here is not enough for you, please check the video (which is in Portuguese).

## Table of Contents




- [1. Prerequisites](#1-prerequisites)
  * [1.1. Install Docker Engine](#11-install-docker-engine)
  * [1.2. Install Git](#12-install-git)
  * [1.3. Install you favorite code editor](#13-install-you-favorite-code-editor)
- [2. Setup](#2-setup)
  * [2.1. Create a new folder to use on the tutorial](#21-create-a-new-folder-to-use-on-the-tutorial)
  * [2.2. Clone the tutorial complete code](#22-clone-the-tutorial-complete-code)
  * [2.3. Create a new folder to do the follow-trough of the tutorial](#23-create-a-new-folder-to-do-the-follow-trough-of-the-tutorial)
  * [2.4. Inicialize Git](#24-inicialize-git)
- [3. Docker](#3-docker)
  * [3.1. Copy the Dockerfile-zero from the complete code](#31-copy-the-dockerfile-from-the-complete-code)
  * [3.1. Build Docker Image from Dockerfile](#31-build-docker-image-from-dockerfile)
  * [3.2. Run the Docker container (Linux)](#32-run-the-docker-container-linux)
  * [3.3. Run the Docker container (Windows)](#33-run-the-docker-container-windows)
  * [3.4. Open a bash in the container](#34-open-a-bash-in-the-container)
- [4. Kedro](#4-kedro)
  * [4.1. Check Kedro installation](#41-check-kedro-installation)
  * [4.2. Create a Kedro Project](#42-create-a-kedro-project)
  * [4.3. Move files properly](#43-move-files-properly)
  * [4.4. Initialize MLFlow plugin](#44-initialize-mlflow-plugin)
  * [4.5 Copy the utils folder from the complete code](#45-copy-the-utils-folder-from-the-complete-code)
  [4.6 Copy the conf folder from the complete code](#45-copy-the-conf-folder-from-the-complete-code)
  [4.7 Copy the notebooks folder from the complete code](#45-copy-the-notebooks-folder-from-the-complete-code)
  * [4.8. Run Jupyter Server](#46-run-jupyter-server)
  * [4.9. Run Kedro Viz](#47-run-kedro-viz)
- [5. MLFlow](#5-mlflow)
  * [5.1. Run MLFlow Server](#51-run-mlflow-server)

## 1. Prerequisites

### 1.1. Install Docker Engine
Follow the instructions [here](https://docs.docker.com/engine/install/) to install Docker Engine for you OS.


### 1.2. Install Git
Follow the instructions [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) to install Git for you OS.

### 1.3. Install you favorite code editor

Choose the code editor of you preference (PyCharm, Atom, VSCode, etc...) to help you following the tutorial.

## 2. Setup

### 2.1. Create a new folder to use on the tutorial

```
mkdir tutorial && cd tutorial
```

### 2.2. Clone the tutorial complete code

```
git clone https://github.com/rodra-go/kedro-mlflow-tutorial.git
```

### 2.3. Create a new folder to do the follow-trough of the tutorial

```
mkdir follow-trough && cd follow-trough
```

### 2.4. Inicialize Git

```
git init
```

## 3. Docker
### 3.1. Copy the Dockerfile from the complete code

```
cp ../kedro-mlflow-tutorial/Dockerfile-zero ./Dockerfile
```

### 3.1. Build Docker Image from Dockerfile

```
docker build -t kedro-mlflow-tutorial:0.1 .
```

### 3.2. Run the Docker container (Linux)

```
docker run --rm --name kedro_mlflow_tutorial -dit -p 4141:4141 -p 8888:8888 -p 5000:5000 -v $(pwd):/usr/src/code/ kedro-mlflow-tutorial:0.1
```

### 3.3. Run the Docker container (Windows)

Replace the ```$(pwd)``` on the command above for the path given by the command ```pwd``` on Windows Power Shell, then run the command.
```pwd``` on Windows Power Shell, then run the command.

```
docker run --rm --name kedro_mlflow_tutorial -dit -p 4141:4141 -p 8888:8888 -p 5000:5000 -v <C:/path/to/tutorial/follow-trough>:/usr/src/code/ kedro-mlflow-tutorial:0.1
```

### 3.4. Open a bash in the container

```
docker exec -it kedro_mlflow_tutorial bash
```

## 4. Kedro

### 4.1. Check Kedro installation

```
kedro info
```

### 4.2. Create a Kedro Project

```
kedro new
```

Name your project ```Kedro MLFlow Tutorial``` (otherwise the code might no work).

### 4.3. Move files properly

```
shopt -s dotglob && mv ./kedro-mlflow-tutorial/* . && rm -rf ./kedro-mlflow-tutorial
```

### 4.4. Initialize MLFlow plugin

```
kedro mlflow init
```

### 4.5 Copy the utils folder from the complete code

```
cp -R ../kedro-mlflow-tutorial/src/kedro_mlflow_tutorial/utils ./src/kedro_mlflow_tutorial/utils
```

### 4.6 Copy the conf folder from the complete code

```
cp -R ../kedro-mlflow-tutorial/conf ./conf
```

### 4.7 Copy the notebooks folder from the complete code

```
cp -R ../kedro-mlflow-tutorial/notebooks ./notebooks
```

### 4.8. Configure your credentials

In order to access the TPN-USP file server and complete the Data Integration implementation, it is necessary to configure your credentials on TPN-USP Network. Add the following lines to your ```./conf/local/credentials.yml``` file:

```
tpn:
  username: <your_user_name>
  password: <your_password>
```

In case you don't have access to TPN-USP network, download the raw data [here](https://drive.google.com/file/d/1lDUEnU10FZRJLh0se3eoLfC5Xnero49_/view?usp=sharing) and extract its contents to ```./data/01_raw``` in your follow-trough directory.


### 4.7. Run Jupyter Server

```
kedro jupyter notebook --ip 0.0.0.0
```

### 4.8. Run Kedro Viz

```
kedro viz --host 0.0.0.0
```

## 5. MLFlow

### 5.1. Run MLFlow Server

```
mlflow ui --host 0.0.0.0 --backend-store-uri file:///usr/src/code/mlruns
```

## Overview

This is your new Kedro project, which was generated using `Kedro 0.16.6`.

Take a look at the [Kedro documentation](https://kedro.readthedocs.io) to get started.

## Rules and guidelines

In order to get the best out of the template:

* Don't remove any lines from the `.gitignore` file we provide
* Make sure your results can be reproduced by following a [data engineering convention](https://kedro.readthedocs.io/en/stable/11_faq/01_faq.html#what-is-data-engineering-convention)
* Don't commit data to your repository
* Don't commit any credentials or your local configuration to your repository. Keep all your credentials and local configuration in `conf/local/`

## How to install dependencies

Declare any dependencies in `src/requirements.txt` for `pip` installation and `src/environment.yml` for `conda` installation.

To install them, run:

```
kedro install
```

## How to run your Kedro pipeline

You can run your Kedro project with:

```
kedro run
```

## How to test your Kedro project

Have a look at the file `src/tests/test_run.py` for instructions on how to write your tests. You can run your tests as follows:

```
kedro test
```

To configure the coverage threshold, go to the `.coveragerc` file.

## Project dependencies

To generate or update the dependency requirements for your project:

```
kedro build-reqs
```

This will copy the contents of `src/requirements.txt` into a new file `src/requirements.in` which will be used as the source for `pip-compile`. You can see the output of the resolution by opening `src/requirements.txt`.

After this, if you'd like to update your project requirements, please update `src/requirements.in` and re-run `kedro build-reqs`.

[Further information about project dependencies](https://kedro.readthedocs.io/en/stable/04_kedro_project_setup/01_dependencies.html#project-specific-dependencies)

## How to work with Kedro and notebooks

> Note: Using `kedro jupyter` or `kedro ipython` to run your notebook provides these variables in scope: `context`, `catalog`, and `startup_error`.
>
> Jupyter, JupyterLab, and IPython are already included in the project requirements by default, so once you have run `kedro install` you will not need to take any extra steps before you use them.

### Jupyter
To use Jupyter notebooks in your Kedro project, you need to install Jupyter:

```
pip install jupyter
```

After installing Jupyter, you can start a local notebook server:

```
kedro jupyter notebook
```

### JupyterLab
To use JupyterLab, you need to install it:

```
pip install jupyterlab
```

You can also start JupyterLab:

```
kedro jupyter lab
```

### IPython
And if you want to run an IPython session:

```
kedro ipython
```

### How to convert notebook cells to nodes in a Kedro project
You can move notebook code over into a Kedro project structure using a mixture of [cell tagging](https://jupyter-notebook.readthedocs.io/en/stable/changelog.html#cell-tags) and Kedro CLI commands.

By adding the `node` tag to a cell and running the command below, the cell's source code will be copied over to a Python file within `src/<package_name>/nodes/`:

```
kedro jupyter convert <filepath_to_my_notebook>
```
> *Note:* The name of the Python file matches the name of the original notebook.

Alternatively, you may want to transform all your notebooks in one go. Run the following command to convert all notebook files found in the project root directory and under any of its sub-folders:

```
kedro jupyter convert --all
```

### How to ignore notebook output cells in `git`
To automatically strip out all output cell contents before committing to `git`, you can run `kedro activate-nbstripout`. This will add a hook in `.git/config` which will run `nbstripout` before anything is committed to `git`.

> *Note:* Your output cells will be retained locally.

## Package your Kedro project

[Further information about building project documentation and packaging your project](https://kedro.readthedocs.io/en/stable/03_tutorial/05_package_a_project.html)
