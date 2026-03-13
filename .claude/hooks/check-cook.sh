#!/bin/bash
# Hook: 実装変更があるのにcook/が未更新の場合にリマインドする
# また、taskファイルに対応するlogファイルが存在しない場合も警告する
# UserPromptSubmit イベントで実行 → stdout がClaudeのコンテキストに注入される

cd "${CLAUDE_PROJECT_DIR:-.}"

# git管理外なら何もしない
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
    exit 0
fi

# ステージング済み + 未ステージングの変更ファイル一覧
CHANGED=$(git diff --name-only HEAD 2>/dev/null; git diff --name-only --cached 2>/dev/null; git ls-files --others --exclude-standard 2>/dev/null)

if [ -z "$CHANGED" ]; then
    # 変更がなくてもlogファイル欠落チェックは行う
    :
else
    # cook/ 以外の変更があるか
    HAS_WORK_CHANGES=false
    HAS_COOK_CHANGES=false

    while IFS= read -r file; do
        case "$file" in
            cook/*) HAS_COOK_CHANGES=true ;;
            .gitignore|*.md) ;; # ドキュメントのみの変更は除外
            tests/*|skills/*|.claude/*|input_list.txt|adr/*|styles/*) HAS_WORK_CHANGES=true ;;
        esac
    done <<< "$CHANGED"

    if [ "$HAS_WORK_CHANGES" = true ] && [ "$HAS_COOK_CHANGES" = false ]; then
        echo "[cook リマインダー] 実装変更がありますが cook/ が未更新です。ADR-001に従い、タスクファイルとログファイルを作成してください。"
        echo "  タスク作成: python skills/cook/scripts/init_task.py cook <name>"
        echo "  ログ作成:   python skills/cook/scripts/write_log.py cook <name>"
    fi
fi

# logファイル欠落チェック: taskファイルに対応するlogファイルが存在しない場合に警告
if [ -d "cook" ]; then
    MISSING=""
    for task in cook/*_task.md; do
        [ -f "$task" ] || continue
        log="${task%_task.md}_log.md"
        if [ ! -f "$log" ]; then
            MISSING="$MISSING  - $(basename "$task") に対応するログ: $(basename "$log")\n"
        fi
    done
    if [ -n "$MISSING" ]; then
        echo "[cook 警告] 以下のtaskファイルに対応するlogファイルが未作成です:"
        echo -e "$MISSING"
    fi
fi

exit 0
