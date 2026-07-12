# claude-config

Claude Code 개인 설정 동기화용 dotfiles.

추적 대상: `CLAUDE.md`, `settings.json`, `skills/` (민감파일·캐시·세션은 `.gitignore`로 제외).

## 새 기기 세팅 (예: 맥북)

```bash
# 1. Claude Code 설치 후 로그인
claude        # 실행 → /login (같은 계정)

# 2. 이 repo를 ~/.claude 에 반영
cd ~/.claude
git init
git remote add origin <이 repo URL>
git fetch origin
git checkout -b main --track origin/main   # 기존 파일과 충돌 시 백업 후 진행

# 3. superpowers 플러그인 재설치
# claude 안에서:
#   /plugin marketplace add anthropics/claude-plugins-official
#   /plugin install superpowers
```

## 맥 세팅 시 수정 필요

- **`settings.json` Stop 훅**: `powershell.exe [console]::beep` → `afplay /System/Library/Sounds/Glass.aiff` 로 교체
- **`CLAUDE.md` 개발환경 섹션**: `OS: Windows 11 / Shell: PowerShell` → `OS: macOS / Shell: zsh`

> 두 파일은 OS별로 값이 달라서, 필요하면 브랜치를 나눠 관리해도 됨 (`main`=공통, `windows`/`mac`=OS별).

## 변경 반영

```bash
cd ~/.claude
git add -A && git commit -m "update config" && git push
```
