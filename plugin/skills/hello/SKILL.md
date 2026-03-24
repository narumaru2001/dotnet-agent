---
name: hello
description: 名前を受け取って英語で挨拶を返す
---

# Skill: hello

## 役割
名前を受け取って英語で挨拶を返す。

## パラメータ

| 名前 | 型 | 必須 | 説明 |
|---|---|---|---|
| name | string | はい | 挨拶する相手の名前 |

## 実行例

```bash
python -B run.py '{"name": "Alice"}'
```

## 戻り値

```json
{"result": "Hello, Alice!"}
```
