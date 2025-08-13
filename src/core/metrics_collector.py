# Metrics Collector

import time
from collections import deque

class MetricsCollector:
    def __init__(self):
        """
        Initializes the Metrics Collector for tracking real-time server metrics.
        """
        self.server_start_time = time.time()
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.active_tasks = 0
        self.response_times = deque(maxlen=100) # Store last 100 response times
        print("Metrics Collector initialized.")

    def increment_total_requests(self):
        self.total_requests += 1

    def increment_successful_requests(self):
        self.successful_requests += 1

    def increment_failed_requests(self):
        self.failed_requests += 1

    def task_started(self):
        self.active_tasks += 1

    def task_finished(self):
        if self.active_tasks > 0:
            self.active_tasks -= 1

    def add_response_time(self, response_time: float):
        self.response_times.append(response_time)

    def get_metrics(self) -> dict:
        """
        Calculates and returns the current set of metrics.
        """
        uptime = time.time() - self.server_start_time
        
        avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0
        
        success_rate = (self.successful_requests / self.total_requests) if self.total_requests > 0 else 0

        return {
            "server_status": "online",
            "uptime_seconds": uptime,
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "active_tasks": self.active_tasks,
            "average_response_time_ms": avg_response_time * 1000,
            "success_rate": success_rate
        }
