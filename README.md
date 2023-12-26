# README: OpenAI APIを使用した画像処理と分析

このPythonスクリプトは、OpenAIのGPT-4ビジョンAPIを使用して画像処理と分析を行うために設計されています。スクリプトには、画像エンコーディングの処理、OpenAI APIへのリクエスト送信、単一および比較画像分析のレスポンス処理の機能が含まれています。

## 特徴
- **画像エンコーディング**: ローカルの画像をAPI処理用のBase64形式に変換します。
- **単一画像分析**: 単一の画像を分析し、OpenAI APIからのレスポンスを返します。
- **比較画像分析**: 二つの画像を比較し、分析結果および詳細をAPIから取得します。
- **JSONレスポンスのサポート**: JSON形式でのレスポンスをリクエストおよび処理する機能が含まれています。

## 必要条件
- Python 3
- `openai` Pythonパッケージ
- `requests` Pythonパッケージ
- 環境管理のための`dotenv` Pythonパッケージ

## セットアップ
1. **必要なパッケージをインストール**:
   ```
   pip install openai requests python-dotenv
   ```
2. **`.env`ファイルを設定**:
   - OpenAI APIキーをこのファイルに含めます: `OPENAI_API_KEY=あなたのAPIキー`

## 関数
- `encode_image(image_path)`: ローカル画像をBase64にエンコードします。
- `get_gpt4v_response_from_encoded_image(base64_image, question, model)`: 単一画像をOpenAI APIに送信し、分析します。
- `get_gpt4v_comparison_from_local_images(image_path1, image_path2, question, model)`: 二つの画像を比較分析するために送信します。
- `get_completion_from_messages(messages, model, temperature)`: テキストプロンプトをAPIに送信する一般的な関数です。
- `get_json_from_messages(messages, model, temperature)`: メッセージをAPIに送信し、JSON形式でのレスポンスをリクエストします。

## Promptの概要
- スクリプトは複数のプロンプトをサポートしています。これらは画像分析の精度を高めるために使用されます。
- `query1`と`query2`は、それぞれ単一および複数画像の分析に関する質問を含んでいます。
- `system`プロンプトは、ユーザーの役割を定義し、JSON出力の指示を提供します。
- `query_json`は、APIからの応答をJSON形式で整形するためのテンプレートを提供します。

## 使用方法
- 入力画像とJSONファイルのパスを設定します。
- 関連する関数を呼び出して画像またはテキストを処理します。
- 応答を取得し、必要に応じて使用します。

## 例
```python
image_path = "./data/grape1.png"
base64_image = encode_image(image_path)
response = get_gpt4v_response_from_encoded_image(base64_image, "この画像には何がありますか？")
print(response)
```

## 追加の注意点
- OpenAIのAPIキーが`.env`ファイルに正しく設定されていることを確認してください。
- 特にクエリとモデルのパラメーターに応じて、スクリプトを特定の使用ケース