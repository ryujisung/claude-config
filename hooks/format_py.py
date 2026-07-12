"""PostToolUse 포맷 훅 — Edit/Write로 .py 파일이 바뀌면 ruff format을 돌린다.

ruff 미설치/실행 실패는 조용히 무시 (포맷은 부가 기능이지 차단 사유가 아님).
"""
import sys
import json
import os
import subprocess


def main() -> int:
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except Exception:
        return 0

    tool_input = data.get("tool_input") or {}
    file_path = tool_input.get("file_path") or ""
    if not file_path:
        # PostToolUse 응답 쪽에 경로가 실릴 수도 있음
        file_path = (data.get("tool_response") or {}).get("filePath") or ""

    if not file_path or not file_path.endswith(".py"):
        return 0
    if not os.path.isfile(file_path):
        return 0

    try:
        subprocess.run(
            [sys.executable, "-m", "ruff", "format", file_path],
            capture_output=True,
            timeout=30,
        )
    except Exception:
        pass  # ruff 없거나 실패해도 무시

    return 0


if __name__ == "__main__":
    sys.exit(main())
