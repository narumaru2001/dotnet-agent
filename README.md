# 既存の .NET デスクトップアプリを AI から呼び出せる形にした話

## はじめに

社内には長年使われている .NET デスクトップアプリケーションがあり、業務ロジックやデータアクセスはそこに蓄積されていました。

それらを Web 化したり全面再構築したりするのではなく、**既存資産を活かしたまま AI から呼び出せる形にしたい**、というのが出発点でした。

既存の業務システムには、長年の運用で積み重ねられた例外処理や業務判断が含まれています。そうした資産を捨てて新しく作り直すのではなく、**自然言語という新しい入口を追加する**ことで、既存システムの価値を保ったまま AI と接続することを目指しました。

---

## 解決アプローチ

既存の .NET デスクトップ資産をそのまま AI から利用するために、**業務単位・機能単位・処理単位**の 3 段階で構成しました。

この構成を .NET 開発の感覚で言い換えると、次のようになります。

| AI の構成要素 | .NET 開発での対応 |
|---|---|
| Project Agent | サブプロジェクト |
| Sub Agent | モジュール |
| Skill | function |

Project Agent・Sub Agent・Skill を作る際には、**既存のソースコードそのものが AI にとっての仕様書**になります。

## Agent 構造の自動生成（4つのユーティリティ Skill）

既存の .NET コードから Agent/Skill の構造を手作業で書き起こす必要はありません。
以下の4つのユーティリティ Skill が、既存資産の解析からプラグイン配布までを段階的に自動化します。

| Skill | 役割 |
|---|---|
| **project-agent-creator** | .sln やフォルダ構成を解析し、業務単位の Project Agent（`AGENT.md`）を自動生成する |
| **sub-agent-creator** | モジュール・クラスを解析し、Sub Agent（`SUB_AGENT.md`）と配下の Skill 一覧を自動生成する |
| **function-skill-creator** | 個々の関数・メソッドを解析し、`SKILL.md` と `run.py`（pythonnet 呼び出しコード）を自動生成する |
| **plugin-builder** | 上記で作った Agent 構造を Claude Code Plugin 形式に一括変換し、配布可能な状態にする |

生成の流れは、既存コードの粒度に沿って **プロジェクト → モジュール → 関数** と段階的に進みます。
各 Skill は前段の出力を入力として連鎖するため、「このプロジェクトから Agent を作って」と指示するだけで、解析から Plugin 化までが一気通貫で実行されます。

---

## ディレクトリ構成

全体の構造は、業務単位・機能単位・処理単位で分けています。

```text
dotnet-agent/
├── .claude/
│   ├── CLAUDE.md                         ← プロジェクト設定（ソリューションファイルに相当）
│   ├── agents/
│   │   └── sample_app/                   ← Project Agent（＝サブプロジェクト）
│   │       ├── AGENT.md
│   │       └── sub/
│   │           ├── greeter/              ← Sub Agent（＝モジュール）
│   │           │   ├── SUB_AGENT.md
│   │           │   └── skills/
│   │           │       ├── hello/        ← Skill（＝function）
│   │           │       │   ├── SKILL.md
│   │           │       │   └── run.py
│   │           │       └── greet/
│   │           │           ├── SKILL.md
│   │           │           └── run.py
│   │           └── calculator/
│   │               ├── SUB_AGENT.md
│   │               └── skills/
│   │                   ├── add/
│   │                   │   ├── SKILL.md
│   │                   │   └── run.py
│   │                   └── multiply/
│   │                       ├── SKILL.md
│   │                       └── run.py
│   └── skills/                           ← AI用ユーティリティ Skill
│       ├── plugin-builder/
│       ├── project-agent-creator/
│       ├── sub-agent-creator/
│       └── function-skill-creator/
├── plugin/                               ← Claude Code Plugin の配布物
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── skills/                           ← agents/ から変換された Skill（フラット配置）
│   │   ├── hello/
│   │   ├── greet/
│   │   ├── add/
│   │   └── multiply/
│   ├── lib/
│   │   └── runtime_init.py               ← 共通ランタイム（pythonnet DLL連携）
│   └── README.md
├── dotnet/                               ← .NET ソースコード
│   └── SampleLib/
│       ├── SampleLib.csproj
│       ├── Greeter.cs
│       └── Calculator.cs
├── agent/                                ← サーバ運用時のタスク管理（todo/done）
├── bin/                                  ← ビルド済み .NET DLL
│   └── SampleLib.dll
└── SystemParams.xml                      ← システム設定
```

AI 側から見ると、業務全体を扱う Project Agent があり、その下に機能群を表す Sub Agent があり、さらに最小実行単位として Skill があります。

この構造にしておくことで、AI は「どの業務の」「どの機能の」「どの処理を」呼ぶべきかを段階的に判断できます。
単に function を並べるのではなく、**業務と機能の文脈を持たせた状態で処理を呼べること**が重要でした。

---

## 具体例：SampleLib（Greeter / Calculator）

このリポジトリに含まれるサンプルでは、次のような対応になっています。

```
SampleApp（Project Agent）
  ├── Greeter（Sub Agent）
  │     ├── hello（Skill）   → Greeter.Hello(name)
  │     └── greet（Skill）   → Greeter.Greet(name, language)
  └── Calculator（Sub Agent）
        ├── add（Skill）     → Calculator.Add(a, b)
        └── multiply（Skill）→ Calculator.Multiply(a, b)
```

利用者が「**田中さんに日本語で挨拶して**」と指示すると、AI は次のように動作します。

1. SampleApp という **Project Agent** を選択
2. 挨拶機能を持つ **Greeter Sub Agent** を選択
3. 多言語挨拶の **greet Skill** を実行
4. `run.py` 経由で **SampleLib.dll の Greeter.Greet()** を呼び出し、結果を JSON で返却

```bash
# 実際に実行される処理
python -B run.py '{"name": "田中", "language": "ja"}'
# → {"result": "こんにちは、田中さん！"}
```

利用者から見ると自然言語で依頼しているだけですが、内部では既存の .NET DLL がそのまま動いています。

この方式の良いところは、**利用者には自然言語の入口だけを見せながら、内部では既存システムの責務分離を保てること**です。
AI は業務を理解して処理を選ぶ役割を担い、実際の処理そのものは従来どおり .NET 側が担います。

---

## 実行の仕組み

選択された Skill は、Python の `run.py` を経由して既存の .NET DLL を呼び出します。

```
自然言語入力
  ↓
AI（Claude Code）
  ↓
Skill（SKILL.md で定義）
  ↓
run.py（Python）
  ↓  ← pythonnet で DLL 呼び出し
既存 .NET DLL
  ↓
JSON で返却
```

Python を挟んでいる理由は次のとおりです。

- AI 側と接続しやすく、JSON を共通インターフェースとして扱いやすい
- **pythonnet** を使うことで既存の .NET DLL を直接呼び出せる
- 入出力の整形、例外処理、ログ出力、権限制御を差し込みやすい

この中継層があることで、**AI 側の柔軟さ**と**既存 .NET 資産の安定性**を両立しやすくなりました。

---

## 運用形態

この仕組みは、利用シーンに応じて複数の運用形態を取ることができます。

| 運用形態 | 説明 |
|---|---|
| **サーバー集中実行** | サーバー上で Claude Code を動かし、MCP を通して既存システムや周辺サービスと接続 |
| **タスクキューによる自動処理** | `todo` ファイルをタスクキューとして使い、定型業務をサーバー側で順次処理 |
| **各端末への Plugin 配布** | Claude Code Plugin として配布し、各端末から直接業務機能を呼び出す |

同じ構造を保ったまま、集中運用と分散運用の両方に対応できる点も、この構成の特徴です。
導入先の制約や運用方針に応じて展開方法を変えられるため、実運用に乗せやすい構成でした。

---

## メリット

この構成の主なメリットをまとめます。

- ✅ **既存資産を再利用できる** — 業務ロジックを再実装しなくてよい
- ✅ **AI の責務を明確に分離できる** — 業務選択は AI、業務実行は .NET
- ✅ **段階的に導入できる** — 業務単位・機能単位で少しずつ広げられる
- ✅ **運用形態を用途に応じて選べる** — サーバー集中、Plugin 配布など柔軟に対応
- ✅ **仕様書が不要** — 既存コードがそのまま AI の仕様書になる

特に大きいのは、**AI 導入をきっかけに全面再構築へ進まなくてもよい点**です。
既存システムを活かしながら、小さく始めて広げられるのは、現場ではかなり重要だと感じています。

---

## 注意点

この方式では、次の点を特に慎重に設計する必要があります。

### 認証・権限管理

AI が処理を実行する場合でも、**誰の権限で実行するのかを明確に**しなければなりません。
利用者が本来許可された範囲でのみ処理できるよう、既存の権限管理と連携させます。

### DB 直接接続の禁止

AI から DB へ直接アクセスさせるのではなく、**必ず既存の業務ロジックやデータアクセス層を経由**させることで、既存システムの制御を維持します。
AI に SQL を直接扱わせないことが重要です。

### 暴走防止

AI が実行できる処理を Skill として**明示的に限定**します。
特に更新系・削除系・一括処理については、確認や制限を設ける設計が前提になります。

> AI は便利ですが、実行権限や実行範囲を曖昧にしたまま既存システムへつなぐのは危険です。
> Skill として公開する範囲を明示的に限定し、実行可能な処理を管理する設計が前提になります。

---

## まとめ

既存の .NET デスクトップアプリケーションを全面再構築するのではなく、**既存のソースコードを AI にとっての仕様書として扱い**、Project Agent・Sub Agent・Skill という構造に再構成することで、自然言語から既存業務ロジックを利用できる形にしました。

その結果、既存資産の価値を維持したまま、AI を新しい入口として追加できるようになります。
また、サーバー運用・todo ファイルによる自動処理・Plugin 配布といった複数の運用方法を選べるため、導入先に応じた展開もしやすくなります。

---

## 関連

- [Claude Code](https://docs.anthropic.com/ja/docs/claude-code/overview)
- [pythonnet](https://github.com/pythonnet/pythonnet)
