import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict
from src.const import *

class JobMonitor:
    def __init__(self, logFilePath=None):
        self.logFilePath = logFilePath or LOG_FILE_PATH
        self.logs = self.log_parser()
        self.processed_entries = []

    def log_parser(self):
        """Reads the log file and converts it to DataFrame.
           returns: df -> DataFrame
        """
        df = pd.read_csv(
            self.logFilePath,
            header=None,
            names=SCHEMA,
            skip_blank_lines=True
        )
        df["status"] = df["status"].str.strip()
        df["job"] = df["job"].str.strip()
        df["pid"] = df["pid"].astype(str).str.strip()
        df["datetime"] = pd.to_datetime(df["time"], format=TIME_FORMAT)
        return df
    
    
    def process_jobs(self):
        """Take Start and End Events in order to calculate the time it takes to finish each task or job.
            returns: list of the results for each of the job
        """
        
        grouped = self.logs.groupby("pid")

        for pid, group in grouped:
            group_sorted = group.sort_values("datetime")
            task_name = group_sorted["job"].iloc[0]

            starts = group_sorted[group_sorted["status"] == Status.START.value]
            ends = group_sorted[group_sorted["status"] == Status.END.value]

            if len(starts) > 1:
                print(f"[WARNING] Multiple START entries for PID {pid} (Task: {task_name}). Default to use just one of them - first one comes.")

            if len(ends) > 1:
                print(f"[WARNING] Multiple END entries for PID {pid} (Task: {task_name}). Default to use just one of them - first one comes.")


            if not starts.empty and not ends.empty: # we calculate the time the run to finish
                start_time = starts.iloc[0]["datetime"]
                end_time = ends.iloc[0]["datetime"]
                duration = (end_time - start_time).total_seconds()

                if duration < 0: #we do not support this case. it means something is wrong
                    print(f"[ERROR] Negative duration for PID {pid}. Please check the inputs")
                    continue

                level = Alert.OK.value
                if duration > ERROR_THRESHOLD:
                    level = Alert.ERROR.value
                elif duration > WARNING_THRESHOLD:
                    level = Alert.WARNING.value

                self.processed_entries.append({
                    "pid": pid,
                    "task": task_name,
                    "start_time": start_time.time(),
                    "end_time": end_time.time(),
                    "duration_sec": duration,
                    "status": level
                })

            elif not starts.empty: #edge case of missing end time.
                print(f"[WARNING] No END found for PID {pid} (Task: {task_name}). Please check.")
            elif not ends.empty: # no start time found. 
                print(f"[WARNING] END without START for PID {pid} (Task: {task_name}). Please check,")

        return self.processed_entries
    
    def get_task_info_by_pid(self, pid, entries):
        """Fetch task or job details for a given PID."""
        data = entries or self.processed_entries
        pid = str(pid) 
        for entry in data:
            if entry["pid"] == pid:
                return entry
        return f"[ERROR] No task found for PID {pid}. Please check your input."

    def generate_report(self, entries):
        """Generate and print a report of all processed job durations.
           returns: the entry found
        """
        df = pd.DataFrame(entries)
        if df.empty:
            print("No valid job logs.")
            return

        print("\n--- Job Monitoring Report ---")
        print(df.to_string(index=False))
        print("\n Summary View:")
        print(df["status"].value_counts())

        df.to_csv("job_monitoring.csv", index=False)

def run():
    if not os.path.exists(LOG_FILE_PATH):
        print(f"Log file not found: {LOG_FILE_PATH}")
        return
    jobPredictor = JobMonitor()
    results = jobPredictor.process_jobs()
    jobPredictor.generate_report(results)

    # Example of using get_task_info_by_pid function
    pid_to_query = "62922"  # Example PID
    task_info = jobPredictor.get_task_info_by_pid(pid_to_query, results)
    print(f"\nTask Info for PID {pid_to_query}: {task_info}")

if __name__ == "__main__":
    run()
