import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    limit = 50
    try:
        base = os.environ["GIT_DIR"]
    except KeyError:
        base = ".git"
    for _ in range(limit):
        if os.path.isdir(base):
            return pathlib.Path(os.getcwd() + f"/{base}")
        else:
            os.chdir("..")


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    if os.path.isfile(workdir):
        raise Exception(f"{workdir.name} is not a directory")
    cur_path = os.getcwd()
    try:
        repo_path = f"{workdir}/{os.environ['GIT_DIR']}"
    except KeyError:
        repo_path = f"{workdir}/.git"
    os.makedirs(repo_path)
    os.chdir(repo_path)
    d = {"HEAD": "ref: refs/heads/master\n",
         "config": "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n",
         "description": "Unnamed pyvcs repository.\n"}
    for name in ("HEAD", "config", "description"):
        create_new_file(name, d[name])
    for dir_ in ("objects", "refs"):
        os.mkdir(dir_)
    os.chdir("refs")
    create_new_file("heads", None)
    create_new_file("tags", None)
    os.chdir(cur_path)
    return pathlib.Path(repo_path)


def create_new_file(name, content):
    with open(name, 'w') as f:
        if content:
            f.write(content)
