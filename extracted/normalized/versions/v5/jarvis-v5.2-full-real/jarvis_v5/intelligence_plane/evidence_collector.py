class EvidenceCollector:
    def __init__(self, adapter):
        self.adapter = adapter

    def collect(self, scan: dict, mission: dict):
        return {
            "scan_signals": {
                **scan["signals"],
                "root_exists": scan.get("root_exists", False),
            },
            "critical_files": self.adapter.find_critical_files(scan["sample_files"]),
            "expected_endpoints": self.adapter.critical_endpoints(),
            "notes": self.adapter.infer_notes(mission),
        }
