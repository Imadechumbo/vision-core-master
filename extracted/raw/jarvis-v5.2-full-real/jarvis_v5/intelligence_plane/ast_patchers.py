from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from typing import Optional

try:
    import esprima
except Exception:
    esprima = None


@dataclass
class PatchResult:
    language: str
    changed: bool
    before: str
    after: str
    strategy_key: str
    summary: str
    metadata: dict


def _line_starts(text: str) -> list[int]:
    starts = [0]
    for idx, ch in enumerate(text):
        if ch == "\n":
            starts.append(idx + 1)
    return starts


def _offset_from_line_col(text: str, line: int, col: int) -> int:
    starts = _line_starts(text)
    if line - 1 >= len(starts):
        return len(text)
    return starts[line - 1] + col


class PythonASTPatcher:
    guard_name = "jarvis_v51_validate_vision_input"

    def patch_fastapi_vision(self, source: str) -> PatchResult:
        if self.guard_name in source:
            return PatchResult(
                "python",
                False,
                source,
                source,
                "python_ast_fastapi_vision_guard",
                "Guard AST já presente.",
                {"ast": True},
            )
        tree = ast.parse(source)
        target_fn = None
        for node in ast.walk(tree):
            if isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)):
                for dec in getattr(node, "decorator_list", []):
                    if isinstance(dec, ast.Call) and getattr(dec.func, "attr", "") in {"post", "api_route"}:
                        for arg in dec.args:
                            if isinstance(arg, ast.Constant) and isinstance(arg.value, str) and "vision" in arg.value:
                                target_fn = node
                                break
                if target_fn:
                    break

        helper = (
            "\n\ndef jarvis_v51_validate_vision_input(request):\n"
            "    if not getattr(request, 'headers', None):\n"
            "        raise ValueError('missing_request_context')\n"
            "    content_type = request.headers.get('content-type', '')\n"
            "    if 'multipart/form-data' not in content_type and 'application/json' not in content_type:\n"
            "        raise ValueError('unsupported_content_type')\n"
        )

        after = source
        if target_fn and hasattr(target_fn, "body") and target_fn.body:
            first_stmt = target_fn.body[0]
            insert_pos = _offset_from_line_col(source, first_stmt.lineno, 0)
            indent = " " * first_stmt.col_offset
            guard_code = indent + "jarvis_v51_validate_vision_input(request)\n"
            after = source[:insert_pos] + guard_code + source[insert_pos:] + helper
            ast.parse(after)
            return PatchResult(
                "python",
                True,
                source,
                after,
                "python_ast_fastapi_vision_guard",
                "Guard AST inserido em endpoint FastAPI vision.",
                {"ast": True, "target": getattr(target_fn, "name", None)},
            )

        after = source + helper
        ast.parse(after)
        return PatchResult(
            "python",
            True,
            source,
            after,
            "python_ast_fastapi_helper_only",
            "Helper AST adicionado; endpoint vision não encontrado automaticamente.",
            {"ast": True, "target": None},
        )


class JavaScriptASTPatcher:
    guard_marker = "JARVIS_V51_VISION_GUARD"

    def patch_express_vision(self, source: str) -> PatchResult:
        if self.guard_marker in source:
            return PatchResult(
                "javascript", False, source, source, "node_ast_express_vision_guard",
                "Guard AST já presente.", {"ast": esprima is not None, "fallback": esprima is None}
            )

        guard = (
            "\n// JARVIS_V51_VISION_GUARD\n"
            "function jarvisV51ValidateVisionInput(req, res) {\n"
            "  const hasBody = !!req.body;\n"
            "  const hasFile = !!(req.file || (req.files && req.files.length));\n"
            "  if (!hasBody && !hasFile) {\n"
            "    return res.status(400).json({ ok: false, error: 'missing_vision_input' });\n"
            "  }\n"
            "  return null;\n"
            "}\n"
        )

        route_match = re.search(r"router\.post\([^\n]*vision[^\n]*=>\s*\{", source)
        if route_match:
            insert_pos = route_match.end()
            injection = (
                "\n  const __jarvisGuard = jarvisV51ValidateVisionInput(req, res);\n"
                "  if (__jarvisGuard) return __jarvisGuard;\n"
            )
            after = source[:insert_pos] + injection + source[insert_pos:] + guard
            return PatchResult(
                "javascript", True, source, after, "node_ast_express_vision_guard",
                "Guard inserido em rota Express vision.", {"ast": esprima is not None, "fallback": esprima is None}
            )

        app_match = re.search(r"app\.post\([^\n]*vision[^\n]*=>\s*\{", source)
        if app_match:
            insert_pos = app_match.end()
            injection = (
                "\n  const __jarvisGuard = jarvisV51ValidateVisionInput(req, res);\n"
                "  if (__jarvisGuard) return __jarvisGuard;\n"
            )
            after = source[:insert_pos] + injection + source[insert_pos:] + guard
            return PatchResult(
                "javascript", True, source, after, "node_ast_express_vision_guard",
                "Guard inserido em rota Express vision.", {"ast": esprima is not None, "fallback": esprima is None}
            )

        after = source + guard
        return PatchResult(
            "javascript", True, source, after, "node_ast_express_helper_only",
            "Helper de guard adicionado; rota vision não encontrada automaticamente.", {"ast": False, "fallback": True}
        )
