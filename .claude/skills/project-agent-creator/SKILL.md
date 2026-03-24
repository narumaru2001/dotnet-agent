---
name: project-agent-creator
description: 既存システムのプロジェクト構造を解析して Project Agent の AGENT.md とフォルダ構成を自動生成する
---

# Skill: project-agent-creator

## 役割
既存システムのプロジェクト構造（.sln、フォルダ構成、README 等）を解析して、
業務単位の Project Agent（AGENT.md）とディレクトリ構成を自動生成する。

## トリガー
- 「このプロジェクトから Agent を作って」
- 「Agent 化して」
- 「AGENT.md を生成して」

## 実行手順

### STEP 1: プロジェクト構造の解析
以下のいずれかを入力として受け取る。

- フォルダ構成のテキスト
- ソリューションファイル（.sln）
- README・仕様書

解析して以下を特定する。

| 項目 | 内容 |
|---|---|
| プロジェクト名 | システムの名称 |
| 主な業務ドメイン | 何を管理するシステムか |
| 主要モジュール | フォルダ・クラス・名前空間の一覧 |
| 外部依存 | DB・API・ファイルなど |

### STEP 2: AGENT.md を生成

```markdown
# {プロジェクト名} Agent

## 役割
{業務ドメインの説明}

## 対応する .NET プロジェクト
- アセンブリ: {DLL名}
- 名前空間: {名前空間}

## Sub Agent 一覧

| Sub Agent | 役割 | パス |
|---|---|---|
| {モジュール名} | {責務} | sub/{モジュール名}/ |
```

### STEP 3: 次のアクション
Sub Agent の作成が必要な場合は sub-agent-creator に引き継ぐ。
