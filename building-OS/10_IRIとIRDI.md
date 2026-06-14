# IRIとIRDIの概要と使い分け

IRI（Internationalized Resource Identifier）とIRDI（International Registration Data Identifier）は、どちらもデジタル空間やデータモデルにおいて、データやモノ（アセット）をグローバルに一意に特定するための識別子（Identifier）の規格です。

特にインダストリー4.0やアセット管理シェル（AAS：Asset Administration Shell）、ECLASSといった、製造業のデジタルツインやデータ連携の文脈で、データの意味（セマンティクス）をシステム間で統一するための「共通言語」として頻繁に登場します。

---

## 1. IRI（Internationalized Resource Identifier）とは

IRIは、インターネットでおなじみの **URI（Uniform Resource Identifier）を国際化した拡張版**です（RFC 3987）。

* **特徴**:
  - URIでは基本的にASCII文字（英数字）しか使えませんでしたが、IRIでは日本語や中国語、キリル文字などのUnicode（UTF-8）文字列をそのまま含めることができます。
* **用途**:
  - Web標準技術（Semantic WebやRDFなど）と親和性が高く、Web上でアクセス可能なリソース、ドキュメント、APIエンドポイント、または独自のデータモデル（AASのサブモデルテンプレートなど）を指し示すために広く使われます。
* **具体例**:
  - [https://admin-shell.io/zvei/nameplate/1/0/Nameplate](https://admin-shell.io/zvei/nameplate/1/0/Nameplate)

---

## 2. IRDI（International Registration Data Identifier）とは

IRDIは、主に産業用データ辞書や部品分類標準（ECLASSやIEC CDDなど）で用いられる、**高度に構造化された識別子**です。
ISO/IEC 11179-6、ISO 29002、ISO/IEC 6523といった国際規格に基づいています。

* **特徴**:
  - 文字列の構造自体に「どの組織が、何の目的で定義した、どのバージョンのデータか」という意味が明確に埋め込まれています。
* **用途**:
  - 「ミリメートル」「定格電圧」「メーカー名」といった、製品の属性（プロパティ）や分類クラスそのものの意味を、システム間で1文字のズレもなく完全に一致させるために使われます。

### 具体例の構造分解
たとえば、ECLASSで定義されているプロパティのIRDI `0173-1#02-BAF053#008` は、以下のように構成されています。

```text
 0173 - 1 # 02 - BAF053 # 008
  │     │   │      │        │
  │     │   │      │        └─── ⑤ Version (バージョン番号: 008)
  │     │   │      └──────────── ④ Concept Code (固有の6桁コード: BAF053)
  │     │   └─────────────────── ③ CSI: Code Space Identifier (オブジェクトの種類: 02=プロパティ, 01=分類クラス等)
  │     └─────────────────────── ② OI: Organization Identifier (組織の識別子: 1)
  └───────────────────────────── ① ICD: International Code Designator (発行組織の種類: 0173=ECLASS, 0112=ISO等)
```

* **`0173`**: **ICD（International Code Designator）**：発行組織の種類（0173はECLASS、0112はISOなど）
* **`1`**: **OI（Organization Identifier）**：組織の識別子
* **`#02`**: **CSI（Code Space Identifier）**：オブジェクトの種類（02はプロパティ、01は分類クラスなど）
* **`-BAF053`**: **Concept Code**：固有の6桁のコード
* **`#008`**: **Version**：バージョン番号

---

## 3. AAS（アセット管理シェル）における違いと使い分け

デジタルツインの相互運用性を確保するAASでは、要素の「意味」を紐付ける `semanticId` などにIRIとIRDIの両方が使われますが、それぞれの役割は以下のように整理できます。

| 項目 | IRI (Internationalized Resource Identifier) | IRDI (International Registration Data Identifier) |
| :--- | :--- | :--- |
| **出自の背景** | Web標準（IETF / W3C） | 産業標準・データ交換（ISO / IEC） |
| **主な対象** | Web上のリソース、アセット自体、カスタムデータモデル | 共通データ辞書（ECLASS, IEC CDD）のクラスやプロパティ |
| **アプローチ** | URLベースで、拡張性や既存のWebシステムとの親和性が高い | 厳密なコード体系で、製造業の部品仕様やカタログデータの機械処理に向く |
| **AASでの典型例** | サブモデルやアセットそのもののグローバルID<br>（例: `https://...`） | 属性のセマンティックID<br>（例: 「ミリメートル」を指す `0173-1#05-AAA480#002`） |

---

## 💡 データ連携における最近のトレンド

最近では、IRDIのコード体系をURLに内包したIRI（例：[https://api.eclass-cdp.com/0173-1-02-AAC895-008](https://api.eclass-cdp.com/0173-1-02-AAC895-008)）を用いて、Webの仕組み（REST APIなど）を介してデータ辞書を直接引きやすくするような、**両者を融合したアプローチ**も一般的になっています。
