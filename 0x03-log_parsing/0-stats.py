#!/usr/bin/python3
import sys
import re

# Define status codes and initialize metrics
STATUS_CODES = [200, 301, 400, 401, 403, 404, 405, 500]
status_counts = {code: 0 for code in STATUS_CODES}
total_file_size = 0
line_count = 0

try:
    for line in sys.stdin:
        # Regex pattern to match the expected format
        pattern = r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - \[(.*)\] "GET /projects/260 HTTP/1\.1" (\d{3}) (\d+)'
        match = re.match(pattern, line.strip())
        
        if match:
            ip_address, date, status_code, file_size = match.groups()
            status_code = int(status_code)
            file_size = int(file_size)
            
            # Update metrics
            total_file_size += file_size
            status_counts[status_code] += 1
            line_count += 1
            
            # Print metrics every 10 lines or upon interruption
            if line_count % 10 == 0:
                print(f"Total file size: {total_file_size}")
                for code in sorted(status_counts.keys()):
                    if status_counts[code] > 0:
                        print(f"{code}: {status_counts[code]}")
                print()

except KeyboardInterrupt:
    pass  # Catch KeyboardInterrupt to exit gracefully

finally:
    # Print final metrics upon completion or interruption
    print(f"Total file size: {total_file_size}")
    for code in sorted(status_counts.keys()):
        if status_counts[code] > 0:
            print(f"{code}: {status_counts[code]}")
