"""Proof by failure: crash the disk at EVERY byte offset and check what survives.

Invariant: every write acknowledged before the crash is readable after reboot.
"""
import unittest

from wal import FakeDisk, NaiveStore, WalStore, run

OPS = [(f"user:{i}", f"balance={i * 100}") for i in range(6)] + [("user:0", "balance=999")]


def total_bytes(store_cls) -> int:
    d = FakeDisk()
    run(store_cls, d, OPS)
    return d.bytes_written


def lost_acked_writes(store_cls, crash_at: int):
    disk = FakeDisk(crash_after=crash_at)
    acked = run(store_cls, disk, OPS)
    after = store_cls(disk.reboot()).data
    expected = dict(acked)
    return {k: v for k, v in expected.items() if after.get(k) != v}, acked, after


class TestWal(unittest.TestCase):
    def test_simulate_failure_naive_rewrite_loses_acknowledged_writes(self):
        """Negative control: without a log, some crash point destroys data the client was told was saved."""
        bad = []
        for n in range(total_bytes(NaiveStore) + 1):
            lost, acked, _ = lost_acked_writes(NaiveStore, n)
            if lost:
                bad.append((n, len(acked), len(lost)))
        self.assertTrue(bad, "naive store should lose acknowledged data at some crash point")
        worst = max(bad, key=lambda b: b[2])
        print(f"\n  naive: {len(bad)} of {total_bytes(NaiveStore) + 1} crash points lose acked data; "
              f"worst: crash at byte {worst[0]} loses {worst[2]} of {worst[1]} acked keys")

    def test_recovery_wal_keeps_every_acknowledged_write_at_every_crash_point(self):
        n_points = total_bytes(WalStore) + 1
        for n in range(n_points):
            with self.subTest(crash_at=n):
                lost, acked, after = lost_acked_writes(WalStore, n)
                self.assertEqual(lost, {})
                # Nothing invented: recovered state must equal some prefix of the op sequence
                # at least as long as what was acked (an unacked but fully written record may survive).
                prefixes = [dict(OPS[:i]) for i in range(len(acked), len(OPS) + 1)]
                self.assertIn(after, prefixes)
        print(f"\n  wal: 0 of {n_points} crash points lose acked data")

    def test_recovery_wal_truncates_torn_tail_and_keeps_writing(self):
        disk = FakeDisk(crash_after=total_bytes(WalStore) - 5)  # die 5 bytes before the end
        run(WalStore, disk, OPS)
        store = WalStore(disk.reboot())
        self.assertGreater(store.discarded_tail_bytes, 0)
        store.set("user:7", "balance=700")
        self.assertEqual(WalStore(store.disk.reboot()).data["user:7"], "balance=700")

    def test_recovery_wal_checksum_stops_at_corrupted_record(self):
        disk = FakeDisk()
        run(WalStore, disk, OPS)
        disk.files["wal.log"][20] ^= 0xFF          # flip a byte inside the first record's payload
        store = WalStore(disk.reboot())
        self.assertEqual(store.recovered_records, 0)  # never apply a record you cannot verify


if __name__ == "__main__":
    unittest.main()
