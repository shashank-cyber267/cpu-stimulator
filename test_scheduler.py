import unittest
from app import (
    schedule_fcfs, 
    schedule_sjf_non_preemptive, 
    schedule_srtf_preemptive,
    schedule_priority_non_preemptive,
    schedule_priority_preemptive,
    schedule_round_robin,
    compute_metrics
)

class TestCPUScheduler(unittest.TestCase):

    def test_fcfs_basic(self):
        procs = [
            {'id': 'P1', 'arrival': 0, 'burst': 4, 'priority': 1},
            {'id': 'P2', 'arrival': 1, 'burst': 3, 'priority': 2},
        ]
        sched = schedule_fcfs(procs)
        metrics = compute_metrics(procs, sched)
        # P1: start 0, end 4 (TAT=4, WT=0)
        # P2: start 4, end 7 (TAT=6, WT=3)
        self.assertEqual(metrics['average_waiting_time'], 1.5)
        self.assertEqual(metrics['average_turnaround_time'], 5.0)

    def test_fcfs_idle(self):
        procs = [
            {'id': 'P1', 'arrival': 0, 'burst': 2, 'priority': 1},
            {'id': 'P2', 'arrival': 5, 'burst': 3, 'priority': 2},
        ]
        sched = schedule_fcfs(procs)
        metrics = compute_metrics(procs, sched)
        # P1 ends at 2. Idle from 2 to 5. P2 starts at 5, ends at 8.
        self.assertTrue(any(s['pid'] == 'IDLE' and s['start'] == 2 and s['end'] == 5 for s in sched))
        self.assertEqual(metrics['metrics'][1]['waiting_time'], 0)
        self.assertEqual(metrics['metrics'][1]['turnaround_time'], 3)

    def test_sjf_non_preemptive(self):
        procs = [
            {'id': 'P1', 'arrival': 0, 'burst': 7, 'priority': 1},
            {'id': 'P2', 'arrival': 2, 'burst': 4, 'priority': 1},
            {'id': 'P3', 'arrival': 4, 'burst': 1, 'priority': 1},
            {'id': 'P4', 'arrival': 5, 'burst': 4, 'priority': 1},
        ]
        sched = schedule_sjf_non_preemptive(procs)
        metrics = compute_metrics(procs, sched)
        # At t=0, only P1 is available -> executes 0..7.
        # At t=7, available are P2(4), P3(1), P4(4) -> P3 executes 7..8.
        # At t=8, P2(4) executes 8..12.
        # At t=12, P4(4) executes 12..16.
        seq = [s['pid'] for s in sched if not s['is_idle']]
        self.assertEqual(seq, ['P1', 'P3', 'P2', 'P4'])

    def test_round_robin(self):
        procs = [
            {'id': 'P1', 'arrival': 0, 'burst': 5, 'priority': 1},
            {'id': 'P2', 'arrival': 1, 'burst': 3, 'priority': 1},
            {'id': 'P3', 'arrival': 2, 'burst': 1, 'priority': 1},
        ]
        sched = schedule_round_robin(procs, quantum=2)
        metrics = compute_metrics(procs, sched)
        # t=0: P1 runs [0, 2] (rem=3). Queue at t=2: [P2, P3, P1]
        # t=2: P2 runs [2, 4] (rem=1). Queue at t=4: [P3, P1, P2]
        # t=4: P3 runs [4, 5] (rem=0). Queue at t=5: [P1, P2]
        # t=5: P1 runs [5, 7] (rem=1). Queue at t=7: [P2, P1]
        # t=7: P2 runs [7, 8] (rem=0). Queue at t=8: [P1]
        # t=8: P1 runs [8, 9] (rem=0).
        seq = [s['pid'] for s in sched if not s['is_idle']]
        self.assertEqual(seq, ['P1', 'P2', 'P3', 'P1', 'P2', 'P1'])

if __name__ == '__main__':
    unittest.main()
