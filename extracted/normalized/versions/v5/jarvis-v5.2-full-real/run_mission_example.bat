@echo off
python apps\cli\jarvis.py project add technetgame --root "examples\technetgame_backend_mock" --stack node_express
python apps\cli\jarvis.py mission "corrigir vision do technetgame" --project technetgame --dry-run
