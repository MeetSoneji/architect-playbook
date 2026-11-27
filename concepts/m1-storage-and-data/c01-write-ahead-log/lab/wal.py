"""A key-value store two ways, on a disk that can lose power at any byte.

NaiveStore rewrites its whole state file in place on every write.
WalStore appends each write to a log as [length][crc32][payload] and replays it on start.
The difference between them is the whole lesson of write-ahead logging.
"""
from __future__ import annotations

import json
import struct
import zlib


class Crash(Exception):
    """Power loss. Everything after this byte never reached the disk."""


class FakeDisk:
    """Durable storage that persists bytes in order and can crash after `crash_after` bytes.

    A real disk is messier (sector-sized atomic writes, reordering by the page cache, fsync
    semantics), but "the write stopped somewhere in the middle" is the failure WAL exists for.
    """

    def __init__(self, crash_after: int | None = None):
        self.files: dict[str, bytearray] = {}
        self.budget = crash_after
        self.bytes_written = 0

    def _spend(self, n: int) -> int:
        """Return how many of n bytes may be written before the crash."""
        if self.budget is None:
            self.bytes_written += n
            return n
        allowed = max(0, min(n, self.budget - self.bytes_written))
        self.bytes_written += allowed
        return allowed

    def truncate(self, name: str, size: int = 0) -> None:
        if self.budget is not None and self.bytes_written >= self.budget:
            raise Crash()
        f = self.files.setdefault(name, bytearray())
        del f[size:]

    def append(self, name: str, data: bytes) -> None:
        ok = self._spend(len(data))
        self.files.setdefault(name, bytearray()).extend(data[:ok])
        if ok < len(data):
            raise Crash()

    def read(self, name: str) -> bytes:
        return bytes(self.files.get(name, b""))

    def reboot(self) -> "FakeDisk":
        """Same platters, power back on, no crash scheduled."""
        d = FakeDisk()
        d.files = {k: bytearray(v) for k, v in self.files.items()}
        return d


class NaiveStore:
    """Rewrite-in-place: truncate the file, write the new full state. Looks fine until power fails."""

    FILE = "state.json"

    def __init__(self, disk: FakeDisk):
        self.disk = disk
        try:
            self.data = json.loads(disk.read(self.FILE) or b"{}")
        except json.JSONDecodeError:
            self.data = {}  # torn file: everything previously acknowledged is gone

    def set(self, key: str, value: str) -> None:
        self.data[key] = value
        self.disk.truncate(self.FILE, 0)          # <- the old state is destroyed here...
        self.disk.append(self.FILE, json.dumps(self.data).encode())  # <- ...before the new one exists


HEADER = struct.Struct(">II")  # payload length, crc32(payload)


class WalStore:
    """Append-only log. A write is acknowledged only after its full record is on disk."""

    FILE = "wal.log"

    def __init__(self, disk: FakeDisk):
        self.disk = disk
        self.data: dict[str, str] = {}
        self.recovered_records = 0
        self.discarded_tail_bytes = 0
        self._recover()

    def _recover(self) -> None:
        log, pos = self.disk.read(self.FILE), 0
        while pos + HEADER.size <= len(log):
            length, crc = HEADER.unpack_from(log, pos)
            body = log[pos + HEADER.size: pos + HEADER.size + length]
            if len(body) < length or zlib.crc32(body) != crc:
                break                               # torn or corrupt record: the log ends here
            key, value = json.loads(body)
            self.data[key] = value
            self.recovered_records += 1
            pos += HEADER.size + length
        self.discarded_tail_bytes = len(log) - pos
        if self.discarded_tail_bytes:
            self.disk.truncate(self.FILE, pos)      # cut the torn tail so new appends start clean

    def set(self, key: str, value: str) -> None:
        body = json.dumps([key, value]).encode()
        self.disk.append(self.FILE, HEADER.pack(len(body), zlib.crc32(body)) + body)
        # A real implementation calls fsync() here, before acknowledging. Only now is the write durable.
        self.data[key] = value


def run(store_cls, disk: FakeDisk, ops: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """Apply ops until the disk crashes. Return the ops that were acknowledged."""
    acked = []
    try:
        store = store_cls(disk)
        for k, v in ops:
            store.set(k, v)
            acked.append((k, v))
    except Crash:
        pass
    return acked
