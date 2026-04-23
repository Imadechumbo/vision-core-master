#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
organize_vision_core_extracted.py

Organiza a pasta extracted do VISION_CORE_MASTER sem apagar nada.
Fluxo:
1) Garante extracted/raw e extracted/normalized
2) Move tudo que estiver solto em extracted/ para raw/
3) Copia (não move) de raw/ para normalized/ com classificação por versão
4) Itens não reconhecidos vão para normalized/core_fragments/
5) Gera inventory/version_map_auto.md

Uso:
    python organize_vision_core_extracted.py "C:\caminho\VISION_CORE_MASTER\extracted"

Se nenhum caminho for informado, usa a pasta atual.
"""

from __future__ import annotations

import os
import re
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Tuple

VERSION_BUCKETS = [
    "v22",
    "v3",
    "v4",
    "v5",
    "v5_1",
    "v5_2",
    "v5_3",
    "v5_4",
    "v5_4_1",
    "v5_5",
    "v5_5_1",
    "core_fragments",
    "unknown",
]

FRAGMENT_HINTS = {
    "apps",
    "control_plane",
    "integration_plane",
    "intelligence_plane",
    "interface_plane",
    "memory_plan",
    "projects",
    "vision_core",
    "runtime",
    "services",
    "governance",
    "execution",
    "stability",
    "memory",
    "structure",
    "integrations",
    "orchestration",
    "core",
    "cli",
}

def slugify(name: str) -> str:
    name = name.strip().lower()
    name = name.replace(" ", "_")
    name = re.sub(r"[^a-z0-9._-]+", "_", name)
    name = re.sub(r"_+", "_", name).strip("._")
    return name or "item"

def clean_display(name: str) -> str:
    return name[:-4] if name.lower().endswith(".zip") else name

def classify(name: str) -> Tuple[str, str]:
    """
    Retorna (bucket, normalized_name)
    """
    base = slugify(clean_display(name))

    if base in {slugify(x) for x in FRAGMENT_HINTS}:
        return "core_fragments", base

    if "v551" in base or "v55_1" in base or "v5_5_1" in base:
        return "v5_5_1", base
    if "v55" in base or "v5_5" in base or "vision_core_v55" in base:
        return "v5_5", base
    if "v541" in base or "v5_4_1" in base:
        return "v5_4_1", base
    if "v54" in base or "v5_4" in base:
        return "v5_4", base
    if "v53" in base or "v5_3" in base:
        return "v5_3", base
    if "v52" in base or "v5_2" in base:
        return "v5_2", base
    if "v51" in base or "v5_1" in base:
        return "v5_1", base

    if re.search(r"(^|[_-])v5($|[_-])", base) or "jarvis_v5" in base or "jarvis-v5" in base:
        return "v5", base
    if re.search(r"(^|[_-])v4($|[_-])", base) or "jarvis_core_v4" in base or "jarvis-core-v4" in base:
        return "v4", base
    if re.search(r"(^|[_-])v3($|[_-])", base) or "jarvis_core_v3" in base:
        return "v3", base
    if "v22" in base or "jarvis_v22" in base:
        return "v22", base

    # pistas por texto
    if "level2" in base or "level3" in base or "starter" in base:
        return "v3", base
    if "full_real" in base and "5_2" in base:
        return "v5_2", base
    if "opensquad" in base:
        return "v5_4_1", base
    if "node_real_clean" in base:
        return "v5_5_1", base
    if "executavel" in base and "vision_core" in base:
        return "v5_5", base
    if "executavel" in base and "jarvis" in base:
        return "v5", base

    return "core_fragments", base

def ensure_dirs(extracted_root: Path) -> Dict[str, Path]:
    paths = {
        "root": extracted_root,
        "raw": extracted_root / "raw",
        "normalized": extracted_root / "normalized",
    }
    for bucket in VERSION_BUCKETS:
        if bucket in {"core_fragments", "unknown"}:
            path = paths["normalized"] / bucket
        else:
            path = paths["normalized"] / bucket
        paths[bucket] = path

    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return paths

def unique_dest(dest: Path) -> Path:
    if not dest.exists():
        return dest
    stem = dest.stem
    suffix = dest.suffix
    i = 2
    while True:
        candidate = dest.with_name(f"{stem}__dup{i}{suffix}")
        if not candidate.exists():
            return candidate
        i += 1

def move_loose_items_to_raw(extracted_root: Path, raw_dir: Path) -> List[Tuple[str, str]]:
    moved = []
    for item in extracted_root.iterdir():
        if item.name in {"raw", "normalized"}:
            continue
        dest = unique_dest(raw_dir / item.name)
        shutil.move(str(item), str(dest))
        moved.append((item.name, dest.name))
    return moved

def copy_item(src: Path, dest: Path) -> None:
    if src.is_dir():
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest)

def populate_normalized(raw_dir: Path, normalized_dir: Path) -> Dict[str, List[str]]:
    result: Dict[str, List[str]] = {bucket: [] for bucket in VERSION_BUCKETS}
    for item in sorted(raw_dir.iterdir(), key=lambda p: p.name.lower()):
        bucket, normalized_name = classify(item.name)
        target_dir = normalized_dir / bucket
        ext = item.suffix if item.is_file() else ""
        dest = unique_dest(target_dir / f"{normalized_name}{ext}")
        copy_item(item, dest)
        result[bucket].append(dest.name)
    return result

def write_inventory(extracted_root: Path, normalized_map: Dict[str, List[str]]) -> Path:
    inventory_dir = extracted_root.parent / "inventory"
    inventory_dir.mkdir(parents=True, exist_ok=True)
    out = inventory_dir / "version_map_auto.md"

    lines = []
    lines.append("# VERSION MAP AUTO — VISION CORE")
    lines.append("")
    lines.append("Gerado automaticamente pelo script `organize_vision_core_extracted.py`.")
    lines.append("")
    lines.append("## Estrutura")
    lines.append("")
    lines.append("- `extracted/raw/` → dump bruto preservado")
    lines.append("- `extracted/normalized/` → cópia organizada por versão")
    lines.append("")

    for bucket in VERSION_BUCKETS:
        items = normalized_map.get(bucket, [])
        if not items:
            continue
        lines.append(f"## {bucket}")
        lines.append("")
        for item in items:
            lines.append(f"- {item}")
        lines.append("")

    out.write_text("\n".join(lines), encoding="utf-8")
    return out

def main() -> int:
    if len(sys.argv) > 1:
        extracted_root = Path(sys.argv[1]).expanduser().resolve()
    else:
        extracted_root = Path.cwd().resolve()

    if not extracted_root.exists():
        print(f"[ERRO] Pasta não encontrada: {extracted_root}")
        return 1

    paths = ensure_dirs(extracted_root)
    moved = move_loose_items_to_raw(paths["root"], paths["raw"])
    normalized_map = populate_normalized(paths["raw"], paths["normalized"])
    inventory_file = write_inventory(paths["root"], normalized_map)

    print("")
    print("=== ORGANIZAÇÃO CONCLUÍDA ===")
    print(f"Raiz: {paths['root']}")
    print(f"Raw: {paths['raw']}")
    print(f"Normalized: {paths['normalized']}")
    print(f"Inventário: {inventory_file}")
    print("")

    if moved:
        print("Itens movidos para raw/:")
        for old, new in moved:
            print(f" - {old} -> raw/{new}")
        print("")
    else:
        print("Nenhum item solto foi encontrado em extracted/.")
        print("")

    print("Resumo por bucket:")
    for bucket in VERSION_BUCKETS:
        count = len(normalized_map.get(bucket, []))
        if count:
            print(f" - {bucket}: {count}")

    print("")
    print("Observação:")
    print("- O script preserva o dump bruto em raw/")
    print("- A pasta normalized/ recebe cópias organizadas")
    print("- Nada é apagado automaticamente")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
