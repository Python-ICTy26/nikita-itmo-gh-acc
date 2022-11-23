import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    fmt = f"{fmt} {len(data)}"
    info = fmt.encode() + b"\x00" + data
    hsh = hashlib.sha1(info)
    print(fmt.encode() + b"\x00" + data)
    s_hsh = hsh.hexdigest()
    cur_path = os.getcwd()
    if write:
        try:
            print(os.environ["GIT_DIR"])
            pass
        except KeyError:
            root = repo_find()
            os.chdir(f"{root}/objects")
            try:
                os.mkdir(s_hsh[:2])
            except FileExistsError:
                pass
            os.chdir(s_hsh[:2])
            with open(s_hsh[2:], "wb") as f:
                # print(data)
                if type(info) is str or type(zlib.compress(info)) is str:
                    print("idi nahui")
                f.write(zlib.compress(info))
            os.chdir(cur_path)
    return s_hsh


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    # PUT YOUR CODE HERE
    ...


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    ...


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    # PUT YOUR CODE HERE
    ...


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    # PUT YOUR CODE HERE
    ...


def cat_file(obj_name: str, pretty: bool = True) -> None:
    repo_folder = repo_find()
    obj_folder = obj_name[:2]
    obj_hash = obj_name[2:]
    obj_folder_path = f"{repo_folder}/objects/{obj_folder}"
    if os.path.isdir(obj_folder_path):
        # os.chdir(obj_folder_path)
        obj_file_path = f"{obj_folder_path}/{obj_hash}"
        if os.path.exists(obj_file_path):
            # print(obj_folder_path, obj_file_path, obj_folder, repo_folder)
            with open(obj_file_path, "rb") as obj_f:
                if pretty:
                    print(zlib.decompress(obj_f.read()).decode())
                else:
                    print(obj_f.read())
        else:
            print("no such file")
    else:
        print("no such directory")


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    ...


def commit_parse(raw: bytes, start: int = 0, dct=None):
    # PUT YOUR CODE HERE
    ...


# if __name__ == "__main__":
#     contents = "that's what she said"
#     data = contents.encode()
#     expected_sha = "7e774cf533c51803125d4659f3488bd9dffc41a6"
#     sha = hash_object(data, fmt="blob", write=False)
#     a = 0