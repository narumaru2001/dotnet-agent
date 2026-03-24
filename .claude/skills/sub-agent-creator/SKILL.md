---
name: sub-agent-creator
description: 既存システムのモジュール・クラスを解析して Sub Agent の SUB_AGENT.md とフォルダ構成を自動生成する
---

# Skill: sub-agent-creator

## 役割
既存システムのモジュール・クラスを解析して、
Sub Agent の SUB_AGENT.md と配下の Skill 一覧を自動生成する。

## トリガー
- 「このモジュールから Sub Agent を作って」
- 「Sub Agent を生成して」
- project-agent-creator から引き継がれた場合

## 実行手順

### STEP 1: モジュール・クラスの解析
以下のいずれかを入力として受け取る。

- クラスファイル（.cs / .vb）
- モジュールのフォルダ
- 関数・メソッドの一覧テキスト

解析して以下を特定する。

| 項目 | 内容 |
|---|---|
| モジュール名 | クラス名・フォルダ名 |
| 主な責務 | このモジュールが担当する処理 |
| 主要関数 | public なメソッド・関数の一覧 |

### STEP 2: SUB_AGENT.md を生成

```markdown
# {モジュール名} Sub Agent

## 親 Agent
{Project Agent 名}

## 役割
{モジュールの責務}

## トリガーキーワード
{キーワード一覧}

## Skill 一覧

| Skill | 役割 |
|---|---|
| {skill_id} | {メソッドの説明} |
```

### STEP 3: 次のアクション
各 Skill の作成が必要な場合は function-skill-creator に引き継ぐ。
