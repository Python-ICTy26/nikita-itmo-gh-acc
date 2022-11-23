import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find

# from repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    fmt = f"{fmt} {len(data)}"
    info = fmt.encode() + b"\x00" + data
    hsh = hashlib.sha1(info)
    # print(fmt.encode() + b"\x00" + data)
    s_hsh = hsh.hexdigest()
    cur_path = os.getcwd()
    if write:
        # try:
        #     print(os.environ["GIT_DIR"])
        #     pass
        # except KeyError:
        root = repo_find()
        # os.chdir(f"{root}/objects")
        try:
            os.makedirs(root / "objects" / s_hsh[:2])
        except FileExistsError:
            pass
        if os.path.isfile(root / "objects" / s_hsh[:2] / s_hsh[2:]):
            os.chmod(root / "objects" / s_hsh[:2] / s_hsh[2:], 777)
            print("OK")
        with open(root / "objects" / s_hsh[:2] / s_hsh[2:], "wb") as f:
            # print(data)
            if type(info) is str or type(zlib.compress(info)) is str:
                print("smth wrong")
            f.write(zlib.compress(info))
    return s_hsh


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    if 3 < len(obj_name) < 41:
        obj_folder = obj_name[:2]
        obj_file = obj_name[2:]
        obj_folder_path = gitdir / "objects" / obj_folder
        if os.path.isdir(obj_folder_path):
            lst = list(map(lambda x: str(x).split("/")[-2] + str(x).split("/")[-1], pathlib.Path(obj_folder_path).glob(f"{obj_file}*")))
            if len(lst) > 0:
                return lst
    raise Exception(f"Not a valid object name {obj_name}")


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    ...


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    obj_folder = sha[:2]
    obj_hash = sha[2:]
    obj_path = gitdir / "objects" / obj_folder / obj_hash
    # obj_dir = gitdir / "objects" / obj_folder
    if os.path.isfile(obj_path):
        with open(obj_path, "rb") as f:
            all_data = zlib.decompress(f.read())
            raw_fmt, data = all_data[:all_data.find(b"\x00")], all_data[all_data.find(b"\x00") + 1:]
            fmt = raw_fmt.decode()
            return fmt.split()[0], data
    raise Exception(f"{sha} is not object")


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    result = []
    while len(data) != 0:
        mi = data.find(b" ")
        mode = int(data[:mi].decode())
        # mode = 0
        data = data[mi + 1:]
        zi = data.find(b"\x00")
        name = data[:zi].decode()
        data = data[zi + 1:]
        sha = bytes.hex(data[:20])
        data = data[20:]
        res = (mode, name, sha)
        result.append(res)
    return result


def cat_file(obj_name: str, pretty: bool = True) -> None:
    repo_folder = repo_find()
    obj_folder = obj_name[:2]
    obj_hash = obj_name[2:]
    header, content = read_object(obj_name, repo_folder)
    obj_folder_path = f"{repo_folder}/objects/{obj_folder}"
    if os.path.isdir(obj_folder_path):
        # os.chdir(obj_folder_path)
        obj_file_path = f"{obj_folder_path}/{obj_hash}"
        if os.path.exists(obj_file_path):
            if header == "tree":
                result = ""
                tree_files = read_tree(content)
                for f in tree_files:
                    object_type = read_object(f[2], pathlib.Path(".git"))[0]
                    result += str(f[0]).zfill(6) + " "
                    result += object_type + " "
                    result += f[2] + "\t"
                    result += f[1] + "\n"
                print(result, flush=True)
            # print(obj_folder_path, obj_file_path, obj_folder, repo_folder)
            else:
                if pretty:
                    print(content.decode())
                else:
                    print(content)
        else:
            print("no such file")
    else:
        print("no such directory")


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    result = []
    header, data = read_object(tree_sha, gitdir)
    for f in read_tree(data):
        if read_object(f[2], gitdir)[0] == "tree":
            tree = find_tree_files(f[2], gitdir)
            for blob in tree:
                name = f[1] + "/" + blob[0]
                result.append((name, blob[1]))
        else:
            result.append((f[1], f[2]))
    return result


def commit_parse(raw: bytes, start: int = 0, dct=None):
    data = zlib.decompress(raw)
    i = data.find(b"tree")
    return data[i + 5: i + 45]

# if __name__ == "__main__":
#     contents = "that's what she said"
#     data = contents.encode()
#     expected_sha = "7e774cf533c51803125d4659f3488bd9dffc41a6"
#     sha = hash_object(data, fmt="blob", write=True)
#     cat_file(sha, pretty=True)
#     a = 0