from vision_core.runtime.pipeline import VisionPipeline

pipeline = VisionPipeline()

result = pipeline.run("corrigir runtime do technetgame")

print("STATUS:", result.status)

for step in result.steps:
    print(step)