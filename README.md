# Sematic Kernel Workshop

Learn how to build solutions with Semantic Kernel 
in a day.

## Contents

[Workshop contents](TOC.md)

## Requirements

- Workstation

    - [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
    - [Anaconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
    - [VS Code](https://code.visualstudio.com/)

- Cloud

    - [Azure Subscription](https://azure.com)
    - [Github.com Account](https://github.com)

## First Steps

1. Install the software listed in the previous section.
2. Clone this repository to your local workstation.
```
    git clone git@github.com:placerda/sk-workshop.git  
```
3. Open terminal to create and activate conda environment
```
conda create -n workshop python=3.10
```
4. Open the directory where the repository was cloned in terminal.
```
    cd sk-workshop
```
5. Install the required python libraries.
```
    pip install -r requirements.txt
```
6. Add nbstripout filter to git to avoid saving notebooks output.
```
nbstripout --install
```
6. Open VS Code.
```
    code .
```

7. Go to the [VS Code setup](first_steps/vs_code_setup.md) instructions.
