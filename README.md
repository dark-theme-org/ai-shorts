# ai-shorts

## Goal

Project aimed at creating an **Automatic social media channel/page** based on fully *AI content* for image and audio, publishing **short videos** at least 1x/day.

All the functionallity uses *Python* and the infrastructure with *Terraform*, deployed in *AWS* cloud service as an *AWS Lambda* function.

## Cooperate

- Follow the steps through your terminal using the following logic:

  - Clone the repository to your local machine.

  ```terminal
  cd to/your/folder/path
  git clone https://github.com/dark-theme-org/ai-shorts.git
  ```

  - Create a virtual env and install project dependencies

    - If you don't have *virtualenv* installed

        ```terminal
        pip install virtualenv
        ```

    - Launch virtualenv (python version used was **3.9.12**)

        ```terminal
        cd path/to/github/ai-shorts
        virtualenv --python=python3.9.12 .env
        source .env/Scripts/activate
        ```

    - Install packages with specified versions

        ```terminal
        pip install -r requirements.txt
        ```

## Folders

- [ ] *notebooks* <> Playground for initial coding session;
- [ ] *src* <> Main directory where the entire major scope of the project will be stored;
- [ ] *test* <> Space to create unittests from the functions and methods created.

## Files

- [ ] *.gitattributes* <> Control actions in git, passing specific attributes inside the repository;
- [ ] *.gitignore* <> Intentionally targeting extensions that git should ignore when committing to the project;
- [ ] *.pylintrc* <> Clean code rules for code quality validation;
- [ ] *AUTHORS.md* <> Credits to collaborators who actively participated in this project;
- [ ] *CHANGELOG.md* <> File to report main changes over versions/releases;
- [ ] *requirements.txt* <> Library dependencies and their used versions.
