"""PreToolUse 가드 훅 — Bash/PowerShell 명령에서 삭제/이름변경 패턴을 잡아
CLAUDE.md 금기(파일 삭제·이름 변경 금지)를 harness 레벨에서 강제한다.

매칭되면 permissionDecision="ask"를 반환 → 자동 실행 대신 사용자 확인 프롬프트.
(deny가 아니라 ask인 이유: '명시 승인 없이' 금지이므로, 승인하면 통과해야 함.)
"""
import sys
import json
import re

# (정규식, 사람이 읽을 라벨) — 모두 대소문자 무시
PATTERNS = [
    (r"\brm\s",        "rm (파일/디렉터리 삭제)"),
    (r"\bdel\s",       "del (파일 삭제)"),
    (r"\berase\s",     "erase (파일 삭제)"),
    (r"\brmdir\b",     "rmdir (디렉터리 삭제)"),
    (r"\brd\s+/",      "rd (디렉터리 삭제)"),
    (r"Remove-Item",   "Remove-Item (삭제)"),
    (r"\bren\s",       "ren (이름 변경)"),
    (r"\brename\s",    "rename (이름 변경)"),
    (r"Rename-Item",   "Rename-Item (이름 변경)"),
    (r"\bmv\s",        "mv (이동/이름 변경)"),
    (r"\bmove\s",      "move (이동/이름 변경)"),
    (r"Move-Item",     "Move-Item (이동/이름 변경)"),
]
_COMPILED = [(re.compile(p, re.IGNORECASE), label) for p, label in PATTERNS]


def main() -> int:
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except Exception:
        return 0  # 입력 파싱 실패 시 통과 (가드는 막되 망가뜨리진 않는다)

    command = (data.get("tool_input") or {}).get("command", "")
    if not command:
        return 0

    for rx, label in _COMPILED:
        if rx.search(command):
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "ask",
                    "permissionDecisionReason": (
                        f"⚠ 가드: 삭제/이름변경 명령 감지 ({label}). "
                        "CLAUDE.md 금기 — 명시 승인 필요."
                    ),
                }
            }))
            return 0

    return 0  # 위험 패턴 없음 → 통과


if __name__ == "__main__":
    sys.exit(main())
