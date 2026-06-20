import os
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib_fontja  # 日本語フォント対応

def run_univariate_analysis(csv_path, column_name, output_dir):
    # 1. データの読み込み
    if not os.path.exists(csv_path):
        print(f"Error: ファイルが見つかりません: {csv_path}")
        return False
    
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error: CSVの読み込み中にエラーが発生しました: {e}")
        return False
    
    if column_name not in df.columns:
        print(f"Error: 指定されたカラム '{column_name}' がデータセットに存在しません。")
        print(f"利用可能なカラム: {list(df.columns)}")
        return False
    
    # 2. データのクリーニング（数値変換、欠損値処理）
    series = df[column_name]
    original_len = len(series)
    
    # 数値型にキャスト（変換できないものは NaN にする）
    series_numeric = pd.to_numeric(series, errors='coerce')
    nan_count = series_numeric.isna().sum()
    
    if nan_count > 0:
        print(f"Warning: 非数値データまたは欠損値が {nan_count} 件含まれています。これらは除外して分析します。")
        series_numeric = series_numeric.dropna()
        
    if len(series_numeric) == 0:
        print("Error: 分析可能な有効な数値データが存在しません。")
        return False
        
    # 3. 非図式分析（統計量の算出）
    count = len(series_numeric)
    mean_val = series_numeric.mean()
    median_val = series_numeric.median()
    
    # 最頻値の取得（複数ある場合は最初のものを採用）
    mode_series = series_numeric.mode()
    mode_val = mode_series.iloc[0] if not mode_series.empty else np.nan
    
    min_val = series_numeric.min()
    max_val = series_numeric.max()
    val_range = max_val - min_val
    var_val = series_numeric.var()
    std_val = series_numeric.std()
    
    # 四分位数
    q1 = series_numeric.quantile(0.25)
    q3 = series_numeric.quantile(0.75)
    iqr = q3 - q1
    
    # 歪度・尖度
    skew_val = series_numeric.skew()
    kurt_val = series_numeric.kurt()
    
    print("=" * 50)
    print(f" 単変量分析レポート: {column_name}")
    print("=" * 50)
    print(f"データ総数 (有効数/全体): {count} / {original_len}")
    print(f"平均値 (Mean):          {mean_val:.4f}")
    print(f"中央値 (Median):        {median_val:.4f}")
    print(f"最頻値 (Mode):          {mode_val:.4f}")
    print(f"最小値 (Min):           {min_val:.4f}")
    print(f"最大値 (Max):           {max_val:.4f}")
    print(f"範囲 (Range):           {val_range:.4f}")
    print(f"分散 (Variance):        {var_val:.4f}")
    print(f"標準偏差 (Std Dev):     {std_val:.4f}")
    print(f"第1四分位数 (25%):      {q1:.4f}")
    print(f"第3四分位数 (75%):      {q3:.4f}")
    print(f"四分位範囲 (IQR):       {iqr:.4f}")
    print(f"歪度 (Skewness):        {skew_val:.4f}")
    print(f"尖度 (Kurtosis):        {kurt_val:.4f}")
    print("=" * 50)
    
    # 4. 図式分析（グラフのプロットと保存）
    os.makedirs(output_dir, exist_ok=True)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # ヒストグラム
    sns.histplot(series_numeric, kde=True, ax=axes[0], color='skyblue', edgecolor='black')
    axes[0].axvline(mean_val, color='red', linestyle='--', label=f'平均値: {mean_val:.2f}')
    axes[0].axvline(median_val, color='green', linestyle='-', label=f'中央値: {median_val:.2f}')
    axes[0].set_title(f'ヒストグラムと分布曲線 ({column_name})', fontsize=14)
    axes[0].set_xlabel(column_name, fontsize=12)
    axes[0].set_ylabel('度数', fontsize=12)
    axes[0].legend()
    
    # 箱ひげ図
    sns.boxplot(y=series_numeric, ax=axes[1], color='lightgreen')
    axes[1].set_title(f'箱ひげ図 ({column_name})', fontsize=14)
    axes[1].set_ylabel(column_name, fontsize=12)
    
    plt.tight_layout()
    
    # 保存先ファイルの決定
    output_filename = f"univariate_{column_name}.png"
    output_path = os.path.join(output_dir, output_filename)
    plt.savefig(output_path, dpi=150)
    plt.close()
    
    print(f"グラフを保存しました: {output_path}")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CSVの特定カラムに対して単変量分析を行います。")
    parser.add_argument("--input", required=True, help="入力CSVファイルのパス")
    parser.add_argument("--column", required=True, help="分析対象のカラム名")
    parser.add_argument("--output-dir", default=".", help="分析結果画像の出力先ディレクトリ")
    
    args = parser.parse_args()
    
    run_univariate_analysis(args.input, args.column, args.output_dir)
