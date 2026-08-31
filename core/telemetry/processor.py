"""
CUIX Phase 3: Telemetry Processor & Session Feature Aggregator
Processes raw interaction events and extracts telemetry metrics.
"""

from typing import List, Dict, Any

class TelemetryProcessor:
    def __init__(self, events: List[Dict[str, Any]]):
        self.events = sorted(events, key=lambda x: x.get('timestamp', 0))

    def compute_session_metrics(self) -> Dict[str, Any]:
        if not self.events:
            return {
                "click_frequency_per_min": 0.0,
                "avg_dwell_time_ms": 0.0,
                "backtrack_rate": 0.0,
                "scroll_rate_px_per_sec": 0.0,
                "total_events": 0
            }

        start_time = self.events[0].get('timestamp', 0)
        end_time = self.events[-1].get('timestamp', start_time)
        duration_sec = max((end_time - start_time) / 1000.0, 1.0)

        clicks = [e for e in self.events if e.get('eventType') == 'click']
        scrolls = [e for e in self.events if e.get('eventType') == 'scroll']
        backtracks = [e for e in self.events if e.get('eventType') == 'backtrack']

        click_freq = round((len(clicks) / duration_sec) * 60.0, 2)
        backtrack_rate = round(len(backtracks) / max(len(clicks), 1), 2)

        # Dwell times calculation between consecutive clicks
        dwell_times: List[float] = []
        for i in range(1, len(clicks)):
            t_diff = clicks[i]['timestamp'] - clicks[i - 1]['timestamp']
            if 0 < t_diff < 60000:
                dwell_times.append(t_diff)

        avg_dwell = round(sum(dwell_times) / len(dwell_times), 2) if dwell_times else 0.0

        return {
            "session_duration_sec": round(duration_sec, 2),
            "total_events": len(self.events),
            "click_count": len(clicks),
            "scroll_count": len(scrolls),
            "click_frequency_per_min": click_freq,
            "avg_dwell_time_ms": avg_dwell,
            "backtrack_rate": backtrack_rate
        }
