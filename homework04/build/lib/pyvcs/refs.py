import pathlib
import typing as tp


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    ref = pathlib.Path(ref)
    ref_path = gitdir / ref
    with open(ref_path, "w") as f:
        f.write(new_value)


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    if ref_resolve(gitdir, ref) is None:
        return None
    with open(gitdir / name, "w") as f:
        f.write(f"ref: {ref}")


def ref_resolve(gitdir: pathlib.Path, ref_name: str) -> tp.Optional[str]:
    if ref_name == "HEAD":
        ref_name = get_ref(gitdir)

    ref_path = gitdir / ref_name

    if not ref_path.exists():
        return None

    with ref_path.open(mode="r") as f:
        content = f.read()

    return content


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    return ref_resolve(gitdir, "HEAD")


def is_detached(gitdir: pathlib.Path) -> bool:
    ref = "HEAD"
    ref_path = gitdir / ref
    with ref_path.open(mode="r") as f:
        content = str(f.read())
    if content.find("ref") != -1:
        return False
    else:
        return True


def get_ref(gitdir: pathlib.Path) -> str:
    ref = "HEAD"
    ref_path = gitdir / ref
    with ref_path.open(mode="r") as f:
        content = f.read()
    return content[content.find(" ") + 1 :].strip()