---
name: greet
description: 名前と言語を受け取って多言語で挨拶を返す
---

# Skill: greet

## 役割
名前と言語コードを受け取って、指定言語で挨拶を返す。

## パラメータ

| 名前 | 型 | 必須 | 説明 |
|---|---|---|---|
| name | string | はい | 挨拶する相手の名前 |
| language | string | はい | 言語コード（ja, en, fr） |

## 実行例

```bash
python -B run.py '{"name": "太郎", "language": "ja"}'
```

## 戻り値

```json
{"result": "こんにちは、太郎さん！"}
```
