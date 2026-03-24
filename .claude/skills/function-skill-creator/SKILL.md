---
name: function-skill-creator
description: 既存の関数・メソッドを解析して SKILL.md と run.py（pythonnet 使用）を自動生成する
---

# Skill: function-skill-creator

## 役割
既存の関数・メソッドを解析して、
SKILL.md と run.py（pythonnet による DLL 呼び出しコード）を自動生成する。

## トリガー
- 「この関数から Skill を作って」
- 「Skill 化して」
- sub-agent-creator から引き継がれた場合

## 実行手順

### STEP 1: 関数・メソッドの解析
以下のいずれかを入力として受け取る。

- 関数・メソッドのコード（C# / VB.NET）
- 関数名と仕様テキスト

解析して以下を特定する。

| 項目 | 内容 |
|---|---|
| 関数名 | メソッド名 |
| 目的 | この関数が何をするか（1行） |
| 引数 | 名前・型・必須/省略可 |
| 戻り値 | 型・構造 |
| クラス名 | 所属クラス |
| DLL名 | アセンブリ名 |

### STEP 2: SKILL.md を生成

```markdown
---
name: {skill_name}
description: {関数の目的を1行で}
---

# Skill: {skill_name}

## 親 Sub Agent
{sub_agent_name}

## 役割
{関数の目的}

## 対応する元コード
- クラス: {名前空間.クラス名}
- メソッド: {メソッドシグネチャ}
- DLL: {DLL名}

## パラメータ

| 名前 | 型 | 必須 | 説明 |
|---|---|---|---|
| {引数名} | {型} | {はい/いいえ} | {説明} |

## 実行例
python -B run.py '{JSON}'

## 戻り値
{JSON}
```

### STEP 3: run.py を生成
pythonnet で DLL を読み込み、JSON パラメータを受け取って実行する Python スクリプトを生成する。
