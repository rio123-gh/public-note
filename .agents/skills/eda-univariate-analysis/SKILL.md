---
name: eda-univariate-analysis
description: 与えられたデータセット（CSV形式など）の特定のカラムに対して、基本統計量（平均、中央値、最頻値、分散、標準偏差、歪度、尖度）の算出と、ヒストグラムや箱ひげ図などのグラフ描画を行う単変量分析を実行します。
---

# EDA Univariate Analysis Skill

## Overview
このスキルは、データセット（主にCSVファイル）内の単一の数値変数に対して、単変量分析（Univariate Analysis）を実行するための指示とコードテンプレートを提供します。
分析は、数値を対象とした非図式（Non-graphical）分析と、グラフを用いた図式（Graphical）分析の2つの側面からアプローチします。

## Dependencies
- pandas
- matplotlib
- seaborn
- matplotlib-fontja (日本語フォント表示用)

## Quick Start
エージェントは、本スキルを用いて特定のカラムに対する単変量分析を求められた場合、同梱の `scripts/analyze.py` スクリプトを実行するか、または同等の機能を持つコードを生成・実行します。

### スクリプトの実行方法
`uv run` を使用して、プロジェクトの仮想環境でスクリプトを実行します。

```powershell
uv run python .agents/skills/eda-univariate-analysis/scripts/analyze.py --input path/to/dataset.csv --column column_name --output-dir path/to/output
```

## Workflow

### 1. 単変量・非図式分析 (Univariate Non-graphical)
対象の変数について、データを可視化する前に以下の統計数値を算出してコンソールまたはレポートに出力します。
- 代表値と散布度:
  - データ件数 (Count)
  - 平均値 (Mean)
  - 中央値 (Median)
  - 最頻値 (Mode)
  - 最小値 (Min) / 最大値 (Max)
  - 範囲 (Range)
  - 分散 (Variance)
  - 標準偏差 (Standard Deviation)
  - 四分位数 (25%, 50%, 75%)
- 分布の形状:
  - 歪度 (Skewness): 左右の非対称性を示す指標（0に近いほど対称、正は右裾が長い、負は左裾が長い）
  - 尖度 (Kurtosis): 分布の尖り度合いを示す指標（pandasのデフォルトでは正規分布を0とする超過尖度）

### 2. 単変量・図式分析 (Univariate Graphical)
データの全体像や偏り、外れ値を視覚的に捉えるため、以下のプロットを生成して保存します。
- ヒストグラム (Histogram):
  - データの分布と頻度を確認します。適切なビン（Bin）数を設定し、カーネル密度推定（KDE）を重ねて滑らかな分布形状を視覚化します。
- 箱ひげ図 (Boxplot):
  - 最小値、第1四分位数、中央値、第3四分位数、最大値、および外れ値（IQRの1.5倍を超える値）を可視化します。
- 幹葉図 (Stem-and-Leaf Display):
  - テキストベースで簡易的にデータ分布を表す場合、または小規模データの場合に必要に応じてテキスト出力します。

## Common Mistakes
- **日本語文字化け**: グラフのタイトルや軸ラベルに日本語を使用する際、デフォルトのMatplotlib設定では豆腐文字（文字化け）が発生します。必ず `matplotlib-fontja` をインポートして日本語フォントを有効化してください。
- **データ型の不一致**: 対象カラムに非数値データ（文字列や日付など）や欠損値（NaN）が含まれている場合、計算エラーや意図しないプロットになります。事前に数値へのキャストや欠損値処理（ドロップなど）を行ってください。
