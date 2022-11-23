import os
import pathlib
import stat
import time
import typing as tp
import zlib

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref

# from repo import repo_find, repo_create
# from index import update_index, read_index, GitIndexEntry
# from objects import hash_object, cat_file


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    tree = dict()
    res = b""
    for entry in index:
        path = entry.name
        if dirname in path and len(dirname) > 0:
            path = path[path.find(dirname) + len(dirname) + 1:]
        sp = path.split("/")
        if len(sp) == 1:
            res += b"\x00".join([f"100644 {path}".encode(), entry.sha1])
        else:
            k = sp[0]
            try:
                tree[k].append(entry)
            except KeyError:
                tree[k] = [entry]
    for key in list(tree.keys())[::-1]:
        written = write_tree(gitdir, tree[key], key)
        # res = b"\x00".join([f"40000 {key}".encode(), bytes.fromhex(written)]) + res
        res = ("40000 " + key).encode() + b"\x00" + bytes.fromhex(written) + res
    hsh = hash_object(res, "tree", True)
    # save_p = gitdir / "objects" / hsh[:2]
    # if not os.path.exists(save_p):
    #     os.makedirs(save_p)
    # with open(save_p / hsh[2:], "wb") as tf:
    #     # tf.write(res)
    #     fmt = f"tree {len(index)}"
    #     tf.write(zlib.compress(res))
    return hsh


def commit_tree(
        gitdir: pathlib.Path,
        tree: str,
        message: str,
        parent: tp.Optional[str] = None,
        author: tp.Optional[str] = None,
) -> str:
    timestamp = int(time.mktime(time.localtime()))
    offset = -time.timezone
    hours = abs(offset) // 3600
    author_time = str(timestamp) + " {}{:02}{:02}".format("+" if offset > 0 else "-", hours, (hours * 60) % 60)
    data = f"tree {tree}\n"
    if parent:
        data += f"parent {parent}\n"
    data += f"author {author} {author_time}\n"
    data += f"committer {author} {author_time}\n\n{message}\n"
    sha = hash_object(data.encode(), "commit", True)
    return sha


# if __name__ == "__main__":
#     gitdir = repo_find()
#     mode100644 = stat.S_IFREG | stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
#     quote = pathlib.Path("quote.txt")
#     with open(quote, "w") as f1:
#         f1.write("that's what she said")
#     letters = pathlib.Path("alphabeta") / "letters.txt"
#     # os.removedirs(letters)
#     try:
#         os.mkdir("alphabeta")
#     except FileExistsError:
#         pass
#     with open(letters, "w") as f1:
#         f1.write("abcdefg")
#     digits = pathlib.Path("numbers") / "digits.txt"
#     try:
#         os.mkdir("numbers")
#     except FileExistsError:
#         pass
#     with open(digits, "w") as f1:
#         f1.write("1234567890")
#     update_index(gitdir, [quote, letters, digits], write=True)
#     entries = read_index(gitdir)
#     sha = write_tree(gitdir, entries)
#     # self.assertEqual("a9cde03408c68cbb205b038140b4c3a38aa1d01a", sha)
#
#     alphabeta_tree_sha = "7926bf494dcdb82261e1ca113116610f8d05470b"
#     alphabeta_tree_obj = gitdir / "objects" / alphabeta_tree_sha[:2] / alphabeta_tree_sha[2:]
#     # self.assertTrue(alphabeta_tree_obj.exists())
#
#     numbers_tree_sha = "32ad3641a773ce34816dece1ce63cc24c8a514d0"
#     numbers_tree_obj = gitdir / "objects" / numbers_tree_sha[:2] / numbers_tree_sha[2:]
#     expected_output = "\n".join(
#         [
#             "040000 tree 7926bf494dcdb82261e1ca113116610f8d05470b\talphabeta",
#             "040000 tree 32ad3641a773ce34816dece1ce63cc24c8a514d0\tnumbers",
#             "100644 blob 7e774cf533c51803125d4659f3488bd9dffc41a6\tquote.txt",
#         ]
#     )
#     cat_file(sha, pretty=True)
#     a = 0
