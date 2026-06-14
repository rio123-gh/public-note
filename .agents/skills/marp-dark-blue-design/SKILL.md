---
name: marp-dark-blue-design
description: ダークブルーのテーマを適用したMarpスライドを作成します。ダークブルーのテーマと明示されない場合は、このSkillsを利用しないでください。
---

# Marp Dark Blue Design Creator

## Overview
このスキルは、任意のテキストやMarkdownファイルを受け取り、洗練されたダークブルーテーマ（シアン/スカイブルーのアクセントカラー）のMarpスライドに要約・変換するための指示書です。

## Dependencies
特になし。

## Quick Start
エージェントはこのスキルがトリガーされた場合、以下のCSSとフロントマターをスライドの先頭に埋め込み、入力されたテキストをスライドへと整形します。

### スライドテンプレート (Marpフロントマター)
```markdown
---
marp: true
theme: gaia
_class: lead
paginate: true
backgroundColor: #0f172a
color: #e2e8f0
style: |
  section {
    background-color: #0f172a;
    color: #e2e8f0;
    font-family: 'Inter', 'Helvetica Neue', Arial, 'Hiragino Kaku Gothic ProN', Meiryo, sans-serif;
    padding: 40px;
    font-size: 24px;
  }
  h1 {
    color: #38bdf8;
    font-size: 1.8em;
  }
  h2 {
    color: #38bdf8;
    border-bottom: 2px solid #38bdf8;
    font-size: 1.4em;
    padding-bottom: 10px;
  }
  h3 {
    color: #f1f5f9;
    font-size: 1.1em;
  }
  footer {
    font-size: 0.5em;
    color: #64748b;
  }
  a {
    color: #38bdf8;
    text-decoration: none;
  }
  code {
    background: #1e293b;
    color: #38bdf8;
    padding: 2px 6px;
    border-radius: 4px;
  }
  pre code {
    background: #1e293b;
    color: #e2e8f0;
    display: block;
    padding: 10px;
  }
  table {
    font-size: 0.75em;
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
  }
  th {
    background-color: #1e293b;
    color: #38bdf8;
    border: 1px solid #334155;
    padding: 8px;
    text-align: left;
  }
  td {
    border: 1px solid #334155;
    padding: 8px;
  }
  blockquote {
    background: #1e293b;
    border-left: 5px solid #38bdf8;
    padding: 10px;
    margin: 10px 0;
    font-style: italic;
  }
  .highlight {
    color: #38bdf8;
    font-weight: bold;
  }
  .small {
    font-size: 0.8em;
  }
---
```

## Workflow
インプットテキストからスライドを生成する際、エージェントは以下のステップを実行します。

### 1. 入力コンテンツの分析
- インプットテキストの構造（章立て、見出し）を理解し、スライドの全体枚数や構成を計画します。
- スライド全体のタイトルを決定し、タイトルスライド（1枚目）を作成します。タイトルスライドには `_class: lead` を設定します。

### 2. コンテンツの要約とページ分割
- 各スライドに詰め込むテキスト量を調整します（1スライドあたり箇条書きで5〜6行が目安）。
- `---` を使ってスライドを適切に分割します。
- 長い説明文は、箇条書き（`-`）やテーブル（`|`）に変換して視覚的に整理します。

### 3. スタイルの適用とレイアウトの工夫
- 重要な用語や強調したい箇所には `<span class="highlight">重要ワード</span>` や太字を使用します。
- テキストだけのスライドが続くのを避け、表（テーブル）やASCIIアート・フロー図・コードブロックを挿入してメリハリをつけます。

### 4. Marp記法の検証
- Markdown記法がMarpで正しく解釈されるか（特にテーブルやコードブロックの前後での空行の有無など）を確認します。
- 出力は必ず指定されたファイル（`*(marp版).md` など）に書き込みます。

## Common Mistakes
- **1枚のスライドへの詰め込みすぎ**: テキスト量が多すぎると、Marpレンダリング時に文字がスライド外に溢れたり、極端に小さくなったりします。情報量が多い場合はスライドを2枚に分けてください。
- **改行・空行の欠如**: テーブルやリスト、コードブロックの前に空行がないと、Marpのレンダラーで正しくパースされず、表示が崩れる原因になります。要素の前後には必ず空行を入れてください。
- **フロントマターの欠落**: 最初のスライドの先頭に `marp: true` を含むフロントマターが正しく挿入されているか必ず確認してください。
