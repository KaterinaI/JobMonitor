# Job Monitor Application

## Description

Processes job logs to match START/END events, compute durations of completion, and classify performance alerts.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
5. [Running in Docker](#running-in-docker)
6. [Output](#Output)

## Prerequisites

To run this project, you'll need the following:

- **Python 3.10 or higher** (Python 3.10+ recommended)
- **pip** (Python package installer)
- **Docker** (optional, for containerized execution)


## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://your-repository-url.git
   cd job-monitor

## Running in Docker

```bash
docker-compose run --rm app
docker-compose run --rm test
```

## Output

[WARNING] No END found for PID 72029 (Task: scheduled task 333). Please check.
[WARNING] No END found for PID 72897 (Task: scheduled task 016). Please check.

--- Job Monitoring Report ---
  pid               task start_time end_time  duration_sec  status
10515 scheduled task 386   11:38:33 11:40:24         111.0      OK
16168 scheduled task 773   12:02:39 12:02:55          16.0      OK
22003 scheduled task 004   11:55:29 12:06:42         673.0   ERROR
23118 scheduled task 188   11:40:49 11:41:28          39.0      OK
23703 scheduled task 374   12:04:57 12:18:23         806.0   ERROR
24482 scheduled task 672   12:10:38 12:19:14         516.0 WARNING
24799 scheduled task 536   11:51:21 11:51:28           7.0      OK
26831 scheduled task 538   11:46:04 11:48:16         132.0      OK
27222 scheduled task 294   11:50:07 11:56:15         368.0 WARNING
32674 scheduled task 626   11:51:06 11:52:32          86.0      OK
32904 scheduled task 697   11:49:12 11:49:46          34.0      OK
33528 scheduled task 706   11:52:47 11:56:09         202.0      OK
34189 scheduled task 920   11:59:43 12:03:02         199.0      OK
36709 background job djw   11:47:04 11:47:54          50.0      OK
37980 scheduled task 032   11:35:23 11:35:56          33.0      OK
38579 background job you   11:50:09 11:53:42         213.0      OK
39547 scheduled task 051   11:37:53 11:49:22         689.0   ERROR
39860 scheduled task 460   11:53:17 12:13:09        1192.0   ERROR
45135 scheduled task 515   11:37:14 11:49:37         743.0   ERROR
47139 scheduled task 946   11:44:56 11:48:22         206.0      OK
50295 scheduled task 811   11:48:45 11:55:20         395.0 WARNING
52532 background job tqc   12:00:03 12:13:56         833.0   ERROR
55722 background job cmx   11:54:56 11:55:43          47.0      OK
57672 scheduled task 796   11:36:11 11:36:18           7.0      OK
60134 background job ulp   11:41:11 11:41:55          44.0      OK
62401 scheduled task 936   12:05:59 12:16:23         624.0   ERROR
62922 scheduled task 531   12:14:20 12:15:09          49.0      OK
64591 scheduled task 521   11:57:05 11:58:55         110.0      OK
67833 scheduled task 080   11:57:16 12:00:51         215.0      OK
70808 scheduled task 182   11:44:43 12:18:26        2023.0   ERROR
71766 scheduled task 074   11:45:04 11:50:51         347.0 WARNING
75164 scheduled task 173   11:45:47 11:46:51          64.0      OK
81258 background job wmy   11:36:58 11:51:44         886.0   ERROR
81470 background job wiy   12:08:30 12:09:33          63.0      OK
85742 scheduled task 064   11:55:16 12:07:33         737.0   ERROR
86716 background job xfg   11:59:29 12:05:03         334.0 WARNING
87228 scheduled task 268   11:44:25 11:53:53         568.0 WARNING
87570 scheduled task 794   11:53:57 12:01:50         473.0 WARNING
90812 background job dej   11:39:26 11:43:32         246.0      OK
90962 scheduled task 996   11:40:51 11:42:46         115.0      OK
96183 scheduled task 678   11:58:12 12:02:26         254.0      OK
98746 scheduled task 746   12:04:18 12:11:35         437.0 WARNING
99672 background job sqm   11:57:08 12:02:21         313.0 WARNING

 Summary View:
status
OK         24
ERROR      10
WARNING     9
Name: count, dtype: int64

In case we need to get for a specific PID the corresponding information:
Task Info for PID 62922: {'pid': '62922', 'task': 'scheduled task 531', 'start_time': datetime.time(12, 14, 20), 'end_time': datetime.time(12, 15, 9), 'duration_sec': 49.0, 'status': 'OK'}

Also saves the results locally in job_monitoring.csv