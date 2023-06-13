# ai-shorts

## Goal

Project aimed at creating an **Automatic social media channel/page** based on fully *AI content* for image and audio, publishing **short videos** using a cloud entrypoint.

All the code functionallity uses [Python](https://www.python.org/) and the deployment will be using [Github Actions](https://github.com/features/actions) to run project in cloud. The videos will be extracted from a personal [Google Drive](https://www.google.com/intl/pt-br/drive/about.html) and sent to [AWS S3](https://aws.amazon.com/pt/s3/) for storage and backup files.

## Cooperate

- Follow the steps through your terminal using the following logic:

  - Clone the repository to your local machine.

    ```terminal
    cd to/your/folder/path
    git clone https://github.com/dark-theme-org/ai-shorts.git
    ```

  - Create a virtual env and install project dependencies.

    - If you don't have [Miniconda](https://docs.conda.io/en/latest/miniconda.html#linux-installers) installed:

        ```terminal
        bash Miniconda3-latest-Linux-x86_64.sh
        ```

    - Create virtual environment with conda (python-version used was **3.9.12**)

        ```terminal
        cd path/to/github/ai-shorts
        conda create --name=venv python=3.9.12
        ```

    - Launch venv

        ```terminal
        conda activate venv
        ```

    - Install packages with specified versions

        ```terminal
        pip install -r requirements-dev.txt
        ```

  - Run pre-commit to set up the hooks

    ```terminal
    pre-commit install --config .code_quality/.pre-commit-config.yaml
    ```

## Folders

- [ ] *.code_quality* <> Analyze your source code's quality and complexity, keeping your project's code simple, readable, and easier;
- [ ] *.github* <> Houses workflows, including pull request templates and entrypoint runner;
- [ ] *notebooks* <> Playground for initial coding session;
- [ ] *src* <> Main directory where the entire major scope of the project will be stored;
- [ ] *test* <> Space to create unittests from the functions and methods created.

## Files

- [ ] *.gitattributes* <> Control actions in git, passing specific attributes inside the repository;
- [ ] *.gitignore* <> Intentionally targeting extensions that git should ignore when committing to the project;
- [ ] *AUTHORS.md* <> Credits to collaborators who actively participated in this project;
- [ ] *CHANGELOG.md* <> File to report main changes over versions/releases;
- [ ] *requirements-dev.txt* <> Development dependencies and their used versions;
- [ ] *requirements.txt* <> Code functionallity dependencies.
