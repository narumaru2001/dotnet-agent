---
name: plugin-builder
description: agents/ 配下の Agent/Sub Agent/Skill 構造を Claude Code Plugin 形式に変換する
---

# Skill: plugin-builder

## 役割
`.claude/agents/` 配下の AGENT.md / SUB_AGENT.md / SKILL.md 構造を
Claude Code Plugin 形式（`plugin/`）に変換する。

## トリガー
- 「Plugin を作り直して」
- 「Plugin に変換して」
- 「Plugin を再生成して」

## 変換内容

### 入力
```
.claude/agents/{業務}/sub/{モジュール}/skills/{id}/
  ├── SKILL.md
  └── run.py
```

### 出力
```
plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── {skill_id}/
│       ├── SKILL.md
│       ├── run.py
│       └── tests/
├── lib/
│   └── runtime_init.py
└── README.md
```

## 変換ルール

1. agents/ 配下の全 Skill を plugin/skills/ にフラットにコピー
2. SKILL.md に frontmatter（name, description）がなければ付与
3. run.py の DLL パスを plugin/lib/ 経由に修正
4. plugin.json を生成（Skill 一覧を含む）
5. README.md を生成（利用方法を含む）

## 実行手順

```bash
# Step 1: Plugin 形式に変換
python -B scripts/convert_to_plugin.py

# Step 2: パス修正
python -B scripts/fix_plugin_paths.py
```
