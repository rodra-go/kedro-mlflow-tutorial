# Kedro MLFlow Tutorial

## 1. Setup

### 1.1. Create a new folder to use on the tutorial, then enter into it.

```
mkdir tutorial && cd tutorial
```

### 1.2. Clone the tutorial complete code

```
git clone https://github.com/rodra-go/kedro-mlflow-tutorial.git
```

### 1.3. Create a new folder to do the follow-trough of the tutorial, then enter into it.

```
mkdir follow-trough && cd follow-trough
```

### 1.4. Copy the Dockerfile from the complete code

```
cp ../kedro-mlflow-tutorial/Dockerfile .
```

### 1.5. Inicialize Git

```
git init
```

### 1.6. Build Docker Image from Dockerfile

```
docker build -t kedro-mlflow-tutorial:0.1 .
```

### 1.7. Run the Docker container (Linux)

```
docker run --rm --name kedro_mlflow_tutorial -dit -p 4141:4141 -p 8888:8888 -p 5000:5000 -v $(pwd):/usr/src/code/ kedro-mlflow-tutorial:1.0
```

### 1.8. Run the Docker container (windows)

Replace the ```$(pwd)``` on the command above for the path given by the command
```pwd``` on Windows Power Shell, then run the command.


### 1.9. Open a bash in the container

```
docker exec -it kedro_mlflow_tutorial bash
```

## 2. Kedro

### 2.1. Check Kedro installation

```
kedro info
```

### 2.2. Create a Kedro Project

```
kedro new
```

### 2.3. Move files properly

```
shopt -s dotglob && mv ./kedro-mlflow-tutorial/* . && rm -rf ./kedro-mlflow-tutorial
```

### 2.4. Initialize MLFlow plugin

```
kedro mlflow init
```

### 2.5. Run Jupyter Server

```
kedro jupyter notebook --ip 0.0.0.0
```

### 2.6. Run Kedro Viz

```
kedro viz --host 0.0.0.0
```

## 3. MLFlow

### 3.1. Run MLFlow Server

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
