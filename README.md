# ai-shorts

## Motivation

Considering the growing evolution of generative AIs in 2023, we saw them occupying relevance in the most diverse spheres of competence in the modern world: *ChatGPT* became popular due to its friendly interface, generating texts in chat format; *MidJourney* with creative visual representations; etc.

One of the most famous recently created was the image generator called **Stable Diffusion**, a latent text-to-image diffusion model capable of generating photo-realistic images given any text input. Images created by the pre-trained model can be created under many different circumstances, including video compilation of the images created in sync with an audio as input.

## Main Goal

Project aimed at creating an **Automatic social media channel/page** based on fully *AI content* for image and audio using the deep learning text-to-image model *Stable Diffusion* and publishing them as **short videos** using a local entrypoint to it.

All the code functionallity uses [Python](https://www.python.org/) using versioning control strategies to guarantee quality and security of the application, such as [Github Actions](https://github.com/features/actions) and it's custom toolkit. The videos will be extracted from a personal [Google Drive](https://www.google.com/intl/pt-br/drive/about.html) and sent to [AWS S3](https://aws.amazon.com/pt/s3/) for storage/backup files, created using [Terraform](https://www.terraform.io/).

## Quickstart

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

  - Configure ./src folder as PYTHONPATH (bash example)

    ```terminal
    export PYTHONPATH="$PWD/src"
    ```

## How to run

The file `src/main.py` contains a python script used as entrypoint for local running. You can run it as a script (e.g. `cd src` and `python main.py --scope=prod`). The `--scope=prod` is the environment to be deployed onto. It's an optional parameter which default value is `test`. This string can be anything, but only the word `prod` has a different effect, setting the uploaded video privacy as **public**. Everything else will share the video as **unlisted**.

Another way, much easier, is to run the file `release.sh` that add all the necessary for an execution in fewer lines (e.g. `sh release.sh prod`). In this case, always remember that you need to activate you *virtual env* with `conda activate venv` and them run the **.sh** file.

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
- [ ] *release.sh* <> Script to run all the necessary for local entrypoint;
- [ ] *requirements-dev.txt* <> Development dependencies and their used versions;
- [ ] *requirements.txt* <> Code functionallity dependencies.
