# dotnet-agent サンプル

## 概要

既存の .NET DLL を Claude Code から自然言語で呼び出すサンプルプロジェクトです。
SampleLib.dll（Greeter / Calculator）を題材に、Agent / Sub Agent / Skill の構造を示します。

## 実行環境

- Python 3.10+
- pythonnet (`pip install pythonnet`)
- .NET 8.0 Runtime

## 実行ルール

- DB アクセスは必ず Skill（run.py）経由で実行する
- `pip install` による場当たり的な依存追加をしない
- DLL の直接呼び出しはせず、必ず run.py を経由する

## 担当 Agent

| タグ | AGENT.md |
|---|---|
| [sample] | .claude/agents/sample_app/AGENT.md |

## DLL 配置先

`bin/SampleLib.dll`
