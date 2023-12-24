# GPT-4 Vision API ユーティリティ

このリポジトリには、OpenAIのGPT-4 Vision APIを使用して画像を解析するためのユーティリティスクリプトが含まれています。これにより、画像からの情報抽出や、ロボットアームによるつかみ位置の決定などが可能になります。

## 機能

- URLまたはローカルの画像ファイルから画像を読み込み、GPT-4 Vision APIによる解析を実行
- JSON形式での応答を生成
- 画像比較機能を含む複数のAPIエンドポイントへのアクセス

## 使用方法
(追記予定)

### 事前準備

- OpenAIのAPIキーが必要です。`.env`ファイルに`OPENAI_API_KEY`として保存してください。
- 必要なPythonパッケージをインストールしてください。例: `pip install openai dotenv requests`

### スクリプトの実行

`main()`関数は、様々なタイプのAPIリクエストを実行する例を提供しています。使用する前に、画像のURLまたはローカルファイルパスを指定してください。


### APIリクエストのタイプ

1. **URL画像の解析**  
   `get_gpt4v_response_from_image`関数を使用して、URLで指定された画像の解析を行います。

2. **ローカル画像の解析**  
   `get_gpt4v_response_from_encoded_image`関数を使用して、Base64エンコードされたローカル画像の解析を行います。

3. **2つの画像の比較**  
   `get_gpt4v_comparison_from_images`関数を使用して、2つの画像間の違いを比較します。

4. **2つのローカル画像の比較**  
   `get_gpt4v_comparison_from_local_images`関数を使用して、2つのローカル画像間の違いを比較します。

## JSON出力形式

解析結果は、指定されたJSON形式で出力されます。以下に例を示します：

```json
{
  "image_processing_by_gpt4v": {
    "size": "サイズ情報",
    "shape": "形状情報",
    "color": "色情報",
    "surrounding_environment": "周囲環境情報",
    "grasping_rule": "つかみ位置に関するルール",
    "robotic_arm_grasping_position": {
      "x_coordinate": X座標,
      "y_coordinate": Y座標,
      "z_coordinate": Z座標,
      "orientation": "つかみ方向"
    },
    "reasons_of_grasping_position": "つかみ位置の理由"
  }
}
```

---

このREADMEは、スクリプトの基本的な使い方と機能を説明するためのものです。より詳細な情報や例は、スクリプト内のコメントやドキュメントを参照してください。