---
name: add
description: 2つの整数を足し算する
---

# Skill: add

## 親 Sub Agent
calculator

## 役割
2つの整数を受け取って足し算の結果を返す。

## 対応する元コード
- クラス: SampleLib.Calculator
- メソッド: Add(int a, int b)
- DLL: SampleLib.dll

## パラメータ

| 名前 | 型 | 必須 | 説明 |
|---|---|---|---|
| a | int | はい | 1つ目の整数 |
| b | int | はい | 2つ目の整数 |

## 実行例

```bash
python -B run.py '{"a": 3, "b": 5}'
```

## 戻り値

```json
{"result": 8}
```
