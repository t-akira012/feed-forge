#!/bin/bash
# Hook: 実装変更があるのにmake_log/が未更新の場合にリマインドする
# UserPromptSubmit イベントで実行 → stdout がClaudeのコンテキストに注入される

cd "${CLAUDE_PROJECT_DIR:-.}"

# git管理外なら何もしない
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
    exit 0
fi

# ステージング済み + 未ステージングの変更ファイル一覧
CHANGED=$(git diff --name-only HEAD 2>/dev/null; git diff --name-only --cached 2>/dev/null; git ls-files --others --exclude-standard 2>/dev/null)

if [ -z "$CHANGED" ]; then
    exit 0
fi

# make_log/ 以外の変更があるか
HAS_WORK_CHANGES=false
HAS_MAKE_LOG_CHANGES=false

while IFS= read -r file; do
    case "$file" in
        make_log/*) HAS_MAKE_LOG_CHANGES=true ;;
        .gitignore|*.md) ;; # ドキュメントのみの変更は除外
        tests/*|skills/*|.claude/*|input_list.txt|adr/*) HAS_WORK_CHANGES=true ;;
    esac
done <<< "$CHANGED"

if [ "$HAS_WORK_CHANGES" = true ] && [ "$HAS_MAKE_LOG_CHANGES" = false ]; then
    echo "[make-log リマインダー] 実装変更がありますが make_log/ が未更新です。ADR-001に従い、タスクファイルとログファイルを作成してください。"
    echo "  タスク作成: python skills/make-log/scripts/init_task.py make_log <name>"
    echo "  ログ作成:   python skills/make-log/scripts/write_log.py make_log <name>"
fi

exit 0
