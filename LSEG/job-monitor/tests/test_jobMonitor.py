import unittest
import pandas as pd
from src.jobMonitor import JobMonitor
from src.const import Status, Alert, TIME_FORMAT, SCHEMA
import tempfile
import os
from unittest.mock import patch


class TestJobMonitor(unittest.TestCase):

    def setUp(self):
        """Create a temporary log file with some mock entries."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix=".csv")
        self.temp_file.write(
            "11:35:23,scheduled task 032, START,37980\n"
            "11:35:23,scheduled task 032, START,37980\n"#adding duplicates
            "11:35:56,scheduled task 032, END,37980\n"
            "11:35:56,scheduled task 032, END,37980\n"
            "11:36:11,scheduled task 796, START,57672\n"
            "11:36:18,scheduled task 796, END,57672\n"
            "11:36:58,background job wmy, START,81258\n"  
            "11:37:14,scheduled task 515, START,45135\n"  
            "11:37:14,scheduled task 515, END,45136\n" 
        )
        self.temp_file.close()
        self.monitor = JobMonitor(logFilePath=self.temp_file.name)

    def tearDown(self):
        """Clean up temp file."""
        os.unlink(self.temp_file.name)

    def test_log_parser(self):
        df = self.monitor.logs
        self.assertEqual(len(df), 9)
        self.assertIn("datetime", df.columns)
        self.assertEqual(df["status"].iloc[0], Status.START.value)

    def test_process_jobs(self):
        entries = self.monitor.process_jobs()
        self.assertEqual(len(entries), 2)  
        pids = [entry["pid"] for entry in entries]
        self.assertIn("37980", pids)
        self.assertIn("57672", pids)

    def test_duration_calculation(self):
        entries = self.monitor.process_jobs()
        job_a = next(e for e in entries if e["pid"] == "37980")
        self.assertEqual(job_a["duration_sec"], 33)  # 5 minutes

    def test_missing_end(self):
        self.monitor.process_jobs()
        warnings = [e for e in self.monitor.logs["pid"].unique() if e == "57672"]
        self.assertIn("57672", warnings)

    def test_missing_start(self):
        self.monitor.process_jobs()
        unmatched = [e for e in self.monitor.logs["pid"].unique() if e == "45136"]
        self.assertIn("45136", unmatched)

    def test_get_task_info_by_pid(self):
        entries = self.monitor.process_jobs()
        result = self.monitor.get_task_info_by_pid("37980", entries)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["pid"], "37980")

    def test_get_task_info_invalid_pid(self):
        entries = self.monitor.process_jobs()
        result = self.monitor.get_task_info_by_pid("999999", entries)
        self.assertTrue(result.startswith("[ERROR]"))

class TestJobMonitorThresholds(unittest.TestCase):

    @patch("src.jobMonitor.pd.read_csv")
    def test_duration_warning_and_error_thresholds(self, mock_read_csv):
        data = [
            ["11:00:00", "test task", Status.START.value, "123"],
            ["11:06:00", "test task", Status.END.value, "123"], 

            ["12:00:00", "long task", Status.START.value, "456"],
            ["12:11:00", "long task", Status.END.value, "456"],

            ["13:00:00", "short task", Status.START.value, "789"],
            ["13:04:00", "short task", Status.END.value, "789"], 
        ]
        df = pd.DataFrame(data, columns=SCHEMA)
        df["datetime"] = pd.to_datetime(df["time"], format=TIME_FORMAT)
        mock_read_csv.return_value = df

        monitor = JobMonitor()
        results = monitor.process_jobs()

        self.assertEqual(len(results), 3)

        warning = next((r for r in results if r["pid"] == "123"), None)
        error = next((r for r in results if r["pid"] == "456"), None)
        ok = next((r for r in results if r["pid"] == "789"), None)

        self.assertIsNotNone(warning)
        self.assertIsNotNone(error)
        self.assertIsNotNone(ok)

        self.assertEqual(warning["status"], Alert.WARNING.value)
        self.assertEqual(error["status"], Alert.ERROR.value)
        self.assertEqual(ok["status"], Alert.OK.value)

if __name__ == '__main__':
    unittest.main()
