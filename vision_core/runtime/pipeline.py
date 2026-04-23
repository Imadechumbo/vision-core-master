from datetime import datetime


class PipelineResult:
    def __init__(self):
        self.steps = []
        self.status = "UNKNOWN"
        self.data = {}

    def log(self, step, info):
        self.steps.append({
            "step": step,
            "info": info,
            "time": datetime.utcnow().isoformat()
        })


class VisionPipeline:

    def __init__(self):
        self.result = PipelineResult()

    def run(self, mission: str):
        self.result.log("mission", mission)

        data = self.orchestration(mission)
        data = self.diagnosis(data)
        data = self.planning(data)
        data = self.execution(data)
        data = self.validation(data)
        data = self.security(data)
        decision = self.decision(data)

        if decision != "GOLD":
            self.rollback(data)
            self.result.status = "ROLLED_BACK"
        else:
            self.result.status = "GOLD"

        return self.result

    # ---------------- DOMAINS ----------------

    def orchestration(self, mission):
        self.result.log("orchestration", "dispatch mission")
        return {"mission": mission}

    def diagnosis(self, data):
        self.result.log("diagnosis", "analyzing")
        data["diagnosis"] = "ok"
        return data

    def planning(self, data):
        self.result.log("planning", "creating plan")
        data["plan"] = ["step1", "step2"]
        return data

    def execution(self, data):
        self.result.log("execution", "executing plan")
        data["execution"] = "done"
        return data

    def validation(self, data):
        self.result.log("validation", "running gates")
        data["validation"] = "PASS"
        return data

    def security(self, data):
        self.result.log("security", "policy check")
        data["security"] = "ok"
        return data

    def decision(self, data):
        self.result.log("decision", "evaluating")

        if data["validation"] == "PASS":
            return "GOLD"

        return "FAIL"

    def rollback(self, data):
        self.result.log("rollback", "executing rollback")