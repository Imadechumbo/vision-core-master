from difflib import unified_diff


def generate_diff(before: str, after: str, fromfile: str, tofile: str) -> str:
    lines = unified_diff(before.splitlines(keepends=True), after.splitlines(keepends=True), fromfile=fromfile, tofile=tofile)
    return ''.join(lines)
