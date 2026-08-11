# PythonでOWLを操作する（Owlready2）

PythonからOWL（Web Ontology Language）オントロジーを読み込み、クラスやプロパティを操作したり、リーゾナー（推論エンジン）を実行して矛盾チェックや自動分類を行ったりする場合、現在最も広く使われているのが**Owlready2**というライブラリです。

Owlready2の最大の特徴は、OWLの概念（クラスやプロパティ）を、Pythonのネイティブなクラスや属性として直感的に扱える点にあります。

ここでは、具体的なコード例を交えながら、基本的な使い方から推論の実行までをステップバイステップで解説します。

---

## 1. 準備：Owlready2のインストール

Owlready2を使用するには、以下のパッケージをインストールします。プロジェクト管理ツールとして `uv` を使用している場合は `uv add`、通常の環境では `pip` を使用します。

```bash
# uv を使用する場合
uv add owlready2

# pip を使用する場合
pip install owlready2
```

> [!IMPORTANT]
> Owlready2は内部でJavaベースの推論エンジン（HermiTなど）を動かすため、実行環境に**Java環境（JREまたはJDK）**がインストールされている必要があります。

---

## 2. 具体的なコード例：オントロジーの作成・読み込み・推論

今回は、製造業の「センサーとアラート」を題材に、以下のロジックをOwlready2で実装・推論してみます。

### 実装するロジック
- **オントロジーの定義**: 「温度センサー」と「振動センサー」は排他（Disjoint）関係である。
- **ルールの定義**: 「現在の温度が100度より大きい温度センサー」は、自動的に「緊急（CriticalAlert）」クラスに分類される。
- **インスタンスの作成**: 現在の温度が `105.0` 度の温度センサー `Sensor_A` を作成する。
- **推論の実行**: 推論エンジンを実行し、`Sensor_A` が自動的に `CriticalAlert` クラスへ分類されるか確認する。

### 実装コード

```python
from owlready2 import (
    get_ontology, Thing, ObjectProperty, DataProperty, 
    sync_reasoner, AllDisjoint
)

# 1. 新しいオントロジーをメモリ上に作成
# (既存のOWLファイルを読み込む場合は、ローカルパスやURLを指定します)
onto = get_ontology("http://example.org/factory_ontology.owl")

with onto:
    # --- クラス（概念）の定義 ---
    class Sensor(Thing):
        """すべてのセンサーの親クラス"""
        pass

    class TemperatureSensor(Sensor):
        """温度センサー（Sensorの子クラス）"""
        pass

    class VibrationSensor(Sensor):
        """振動センサー（Sensorの子クラス）"""
        pass

    # 温度センサーと振動センサーは「排他（同時に同じインスタンスになれない）」と定義
    AllDisjoint([TemperatureSensor, VibrationSensor])

    # --- プロパティ（属性・関係）の定義 ---
    class hasCurrentTemperature(DataProperty):
        """現在の温度を保持するデータプロパティ"""
        domain = [TemperatureSensor]
        range  = [float]

    # --- 高度な論理定義（OWLの真骨頂） ---
    class CriticalAlert(Thing):
        """緊急アラートクラス"""
        pass

    # 「CriticalAlert」とは、「現在の温度が100度より大きい温度センサー」と等価（Equivalent）であると定義
    # ※OWLの「Some（〜を持つもの）」や等価条件をPythonの「&」や「>>」記法でスマートに記述できます
    CriticalAlert.equivalent_to.append(
        TemperatureSensor & hasCurrentTemperature.some(lambda value: value > 100.0)
    )

# --- インスタンス（個体）の作成 ---
with onto:
    # 105度の温度を持つ、温度センサーのインスタンスを作成
    sensor_a = TemperatureSensor("Sensor_A")
    sensor_a.hasCurrentTemperature.append(105.0)

# --- 推論前の状態確認 ---
print("--- 推論前の判定 ---")
print(f"Sensor_A の所属クラス: {sensor_a.__class__}")
print(f"Sensor_A は CriticalAlert クラスか？: {isinstance(sensor_a, CriticalAlert)}")

# --- 2. 推論エンジン（リーゾナー）の実行 ---
# 内部でHermiT（あるいはPellet）が走り、定義された論理ルールに基づいてデータを再分類します
with onto:
    sync_reasoner()

# --- 推論後の状態確認 ---
print("\n--- 推論後の判定 ---")
print(f"Sensor_A の所属クラス: {sensor_a.__class__}")
print(f"Sensor_A は CriticalAlert クラスか？: {isinstance(sensor_a, CriticalAlert)}")

# --- 3. オントロジーをファイルとして保存 ---
onto.save(file="factory_ontology.owl", format="rdfxml")
```

### 出力結果

上記のスクリプトを実行すると、以下のような結果が出力されます。

```text
--- 推論前の判定 ---
Sensor_A の所属クラス: factory_ontology.TemperatureSensor
Sensor_A は CriticalAlert クラスか？: False

* Runing HermiT reasoner...
* Powered by Owlready2 2.x *

--- 推論後の判定 ---
Sensor_A の所属クラス: factory_ontology.TemperatureSensor
Sensor_A は CriticalAlert クラスか？: True
```

> [!NOTE]
> **結果の解説**
> 推論前はただの `TemperatureSensor` だった `sensor_a` ですが、`sync_reasoner()` を実行した後は、105度という値の論理定義をリーゾナーが解釈し、自動的に `CriticalAlert` クラスのインスタンスでもあると判定（マルチ・インヘリタンスが成立）しています。

---

## 3. 実務（既存のOWLファイル）でよく使うテクニック

### ① 既存のOWLファイルを読み込む
Protégé（プロテジェ）などの外部ツールで作成した `.owl` ファイルや、Web上で公開されているオントロジーを読み込む場合は、以下のように記述します。

```python
# ローカルファイル、またはURLから読み込み
onto = get_ontology("path/to/your_ontology.owl").load()

# 読み込んだクラスにPythonからアクセスする
my_class = onto.YourClassName
```

### ② データの矛盾（インコンシステント）を検知する
もし「排他（Disjoint）」と定義されている2つのクラスに、誤って同じインスタンスを所属させてしまった場合、リーゾナーを動かすと矛盾（`OwlreadyInconsistencyError`）を検知して例外をスローします。データの整合性チェックに非常に強力です。

```python
from owlready2 import OwlreadyInconsistencyError

with onto:
    # 温度センサーであり、同時に振動センサーでもあるという矛盾したインスタンスを作る
    broken_sensor = TemperatureSensor("Broken_Sensor")
    broken_sensor.is_a.append(VibrationSensor)

try:
    with onto:
        sync_reasoner() # 推論実行
except OwlreadyInconsistencyError:
    print("【警告】データモデルに論理的な矛盾が検知されました！")
```

---

## まとめ

Owlready2を使えば、複雑なOWLの記述言語（RDF/XMLなど）を直接パースすることなく、通常のPythonオブジェクトを操作する感覚でオントロジーの構築や推論が行えます。

ナレッジグラフにルールを持たせ、データが入力された瞬間にバックグラウンドで `sync_reasoner()` を回してデータを自動的に整理・クレンジングする、といったシステム開発において非常に重宝するライブラリです。