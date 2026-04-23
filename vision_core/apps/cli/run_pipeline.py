from vision_core.runtime.pipeline import VisionPipeline

pipeline = VisionPipeline()

result = pipeline.run(
    "corrigir runtime do technetgame",
    environment="production",
)

print("STATUS:", result.status)
print("MISSION_ID:", result.data["mission_id"])
print("DIAGNOSIS_ROOT_CAUSE:", result.data["diagnosis"].root_cause)
print("VALIDATION_OUTCOME:", result.data["validation"].outcome)
print("PASS_GOLD:", result.data["validation"].pass_gold)
print("PROMOTION_ALLOWED:", result.data["security"].promotion_allowed)
print("APPLIED_FILES:", result.data["execution_receipt"].applied_files)
print("SNAPSHOT_ID:", result.data["snapshot_id"])
print("")

for step in result.steps:
    print(step)
