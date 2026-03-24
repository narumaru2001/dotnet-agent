# dotnet-agent-sample Plugin

既存の .NET DLL（SampleLib）を自然言語で呼び出す Claude Code Plugin です。

## インストール

```bash
claude plugin install ./plugin
```

## 利用可能な Skill

| Skill | 説明 |
|---|---|
| hello | 名前を受け取って英語で挨拶を返す |
| greet | 名前と言語を受け取って多言語で挨拶を返す |
| add | 2つの整数を足し算する |
| multiply | 2つの整数を掛け算する |

## 前提条件

- Python 3.10+
- pythonnet (`pip install pythonnet`)
- .NET 8.0 Runtime
