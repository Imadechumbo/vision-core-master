from vision_core.diagnosis.contracts import DiagnosisResult
from vision_core.validation.contracts import ValidationResult


class SDDFService:
    def validate(self, mission_id: str, diagnosis: DiagnosisResult, execution_data: dict) -> ValidationResult:
        receipt = execution_data.get("execution_receipt")

        execution_completed = False
        file_count_ok = False
        if receipt is not None:
            execution_completed = receipt.status == "applied"
            file_count_ok = receipt.applied_files >= 1

        gates = {
            "diagnosis_present": diagnosis is not None,
            "execution_completed": execution_completed,
            "snapshot_created": bool(execution_data.get("snapshot_id")),
            "confidence_threshold": diagnosis.confidence >= 0.75,
            "multi_file_supported": file_count_ok,
        }

        findings: list[str] = []
        if not gates["diagnosis_present"]:
            findings.append("Diagnosis result missing")
        if not gates["execution_completed"]:
            findings.append("Execution did not complete")
        if not gates["snapshot_created"]:
            findings.append("Pre-execution snapshot missing")
        if not gates["confidence_threshold"]:
            findings.append("Diagnosis confidence below GOLD threshold")
        if not gates["multi_file_supported"]:
            findings.append("No file operations were applied")

        if (
            not gates["diagnosis_present"]
            or not gates["execution_completed"]
            or not gates["snapshot_created"]
            or not gates["multi_file_supported"]
        ):
            outcome = "FAIL"
            pass_gold = False
        elif all(gates.values()):
            outcome = "GOLD"
            pass_gold = True
        else:
            outcome = "PASS"
            pass_gold = False

        return ValidationResult(
            mission_id=mission_id,
            outcome=outcome,
            pass_gold=pass_gold,
            findings=findings,
            gates=gates,
            metadata={"engine": "SDDFService"},
        )
