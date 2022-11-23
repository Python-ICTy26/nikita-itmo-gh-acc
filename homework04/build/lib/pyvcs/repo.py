import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    workdir = pathlib.Path(workdir)
    try:
        root = os.environ["GIT_DIR"]
    except KeyError:
        root = ".git"

    if os.path.exists(workdir / root):
        return workdir.absolute() / root
    for c_dir in workdir.parents:
        if os.path.exists(c_dir.absolute() / root):
            return c_dir.absolute() / root
    raise Exception("Not a git repository")


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    path = pathlib.Path(workdir)
    if not path.is_dir():
        raise Exception(f"{path.name} is not a directory")

    try:
        root = os.environ["GIT_DIR"]
    except KeyError:
        root = ".git"

    (path / root).mkdir(exist_ok=False, parents=True)
    (path / root / "refs" / "heads").mkdir(exist_ok=True, parents=True)
    (path / root / "refs" / "tags").mkdir(exist_ok=True, parents=True)
    (path / root / "objects").mkdir(exist_ok=True, parents=True)

    with (
        open(path / root / "HEAD", 'w') as head,
        open(path / root / "config", 'w') as config,
        open(path / root / "description", 'w') as description
    ):
        head.write(
            "ref: refs/heads/master\n")
        config.write(
            "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n")
        description.write(
            "Unnamed pyvcs repository.\n")

    return path / root
