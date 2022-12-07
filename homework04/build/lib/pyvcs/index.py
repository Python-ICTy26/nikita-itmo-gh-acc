import hashlib
import operator
import os
import pathlib
import struct
import typing as tp
# from repo import repo_create, repo_find
from pyvcs.objects import hash_object
# from objects import hash_object

class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        to_pack = (self.ctime_s, self.ctime_n, self.mtime_s, self.mtime_n,
                   self.dev, self.ino, self.mode, self.uid, self.gid, self.size)
        return struct.pack(">LLLLLLLLLL", *to_pack) \
            + self.sha1 + struct.pack(">H", self.flags) + self.name.encode() \
            + b"\x00\x00\x00"

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        # try:
        ctime_s, ctime_n, mtime_s, mtime_n, dev, ino, mode, uid, gid, size = struct.unpack(">LLLLLLLLLL", data[:40])
        # except struct.error:
        #     print(data)
        sha1 = data[40:60]
        flags = struct.unpack(">H", data[60:62])[0]
        name = data[62:len(data) - 3].decode()
        return GitIndexEntry(ctime_s, ctime_n, mtime_s, mtime_n, dev, ino, mode, uid, gid, size, sha1, flags, name)


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    res = []
    if os.path.isfile(gitdir / "index"):
        with open(gitdir / "index", "rb") as index:
            index_data = index.read()
            # entries = index_data[12:].split(b"\x00\x00\x00")
            entry = b""
            for byte in index_data[12:]:
                entry += struct.pack(">B", byte)
                ch = entry[-3:]
                if len(entry) > 62 and entry[-3:] == b"\x00\x00\x00":
                    res.append(GitIndexEntry.unpack(entry))
                    entry = b""
    return res


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    # try:
    #     with open(gitdir / "index", "rb") as index:
    #         old_data = index.read()
    # except FileNotFoundError:
    #     old_data = bytes()
    with open(gitdir / "index", "wb") as index:
        data = b""
        inf = (b"DIRC", 2, len(entries))
        data += struct.pack(">4sII", *inf)
        for entry in entries:
            data += entry.pack()
        data += hashlib.sha1(data).digest()
        index.write(data)


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    res = read_index(gitdir)
    for i in res:
        if details:
            print("100644 " + i.sha1.hex() + " 0\t" + i.name, flush=True)
        else:
            print(i.name, flush=True)


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    index_entries = []
    for path in paths:
        print(path.absolute())
        with open(path.absolute(), "rb") as f:
            hsh = hash_object(f.read(), "blob", write=write)
        file_stats = os.stat(pathlib.Path(path))
        obj = GitIndexEntry(ctime_s=int(file_stats.st_ctime), ctime_n=int(file_stats.st_ctime),
                            mtime_s=int(file_stats.st_mtime), mtime_n=int(file_stats.st_ctime),
                            dev=file_stats.st_dev, ino=file_stats.st_ino, mode=file_stats.st_mode,
                            uid=file_stats.st_uid, gid=file_stats.st_gid, size=file_stats.st_size,
                            sha1=bytes.fromhex(hsh), flags=0, name=str(path))
        index_entries.append(obj)
    if write:
        write_index(gitdir, sorted(index_entries, key=lambda x: x.name))


# if __name__ == "__main__":
#     gitdir = repo_find()
#     entries = [
#         GitIndexEntry(
#             ctime_s=1593379228,
#             ctime_n=200331013,
#             mtime_s=1593379228,
#             mtime_n=200331013,
#             dev=16777220,
#             ino=8610507,
#             mode=33188,
#             uid=501,
#             gid=20,
#             size=4,
#             sha1=b"W\x16\xcaY\x87\xcb\xf9}k\xb5I \xbe\xa6\xad\xde$-\x87\xe6",
#             flags=7,
#             name="bar.txt",
#         ),
#         GitIndexEntry(
#             ctime_s=1593379274,
#             ctime_n=535850078,
#             mtime_s=1593379274,
#             mtime_n=535850078,
#             dev=16777220,
#             ino=8610550,
#             mode=33188,
#             uid=501,
#             gid=20,
#             size=7,
#             sha1=b"\x9f5\x8aJ\xdd\xef\xca\xb2\x94\xb8>B\x82\xbf\xef\x1f\x96%\xa2I",
#             flags=15,
#             name="baz/numbers.txt",
#         ),
#         GitIndexEntry(
#             ctime_s=1593379233,
#             ctime_n=953396667,
#             mtime_s=1593379233,
#             mtime_n=953396667,
#             dev=16777220,
#             ino=8610515,
#             mode=33188,
#             uid=501,
#             gid=20,
#             size=4,
#             sha1=b"%|\xc5d,\xb1\xa0T\xf0\x8c\xc8?-\x94>V\xfd>\xbe\x99",
#             flags=7,
#             name="foo.txt",
#         ),
#     ]
#     write_index(gitdir, entries)
#
#     index = gitdir / "index"
#     with index.open(mode="rb") as f:
#         index_data = f.read()
#     expected_index_data = b"DIRC\x00\x00\x00\x02\x00\x00\x00\x03^\xf9\t\x9c\x0b\xf0\xcf\x05^\xf9\t\x9c\x0b\xf0\xcf\x05\x01\x00\x00\x04\x00\x83b\xcb\x00\x00\x81\xa4\x00\x00\x01\xf5\x00\x00\x00\x14\x00\x00\x00\x04W\x16\xcaY\x87\xcb\xf9}k\xb5I \xbe\xa6\xad\xde$-\x87\xe6\x00\x07bar.txt\x00\x00\x00^\xf9\t\xca\x1f\xf0l^^\xf9\t\xca\x1f\xf0l^\x01\x00\x00\x04\x00\x83b\xf6\x00\x00\x81\xa4\x00\x00\x01\xf5\x00\x00\x00\x14\x00\x00\x00\x07\x9f5\x8aJ\xdd\xef\xca\xb2\x94\xb8>B\x82\xbf\xef\x1f\x96%\xa2I\x00\x0fbaz/numbers.txt\x00\x00\x00^\xf9\t\xa18\xd3\xad\xbb^\xf9\t\xa18\xd3\xad\xbb\x01\x00\x00\x04\x00\x83b\xd3\x00\x00\x81\xa4\x00\x00\x01\xf5\x00\x00\x00\x14\x00\x00\x00\x04%|\xc5d,\xb1\xa0T\xf0\x8c\xc8?-\x94>V\xfd>\xbe\x99\x00\x07foo.txt\x00\x00\x00k\xd6q\xa7d\x10\x8e\x80\x93F]\x0c}+\x82\xfb\xc7:\xa8\x11"
#     # self.assertEqual(expected_index_data, index_data)
#     a = 0
