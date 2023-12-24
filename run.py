import openai
import json
import os
from dotenv import load_dotenv
import tiktoken
import time
import base64
import requests

# .envファイルの内容を読み込む
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

# URLか、ローカルか選択



# 画像をエンコードする関数
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def get_completion_from_messages(messages, model="gpt-3.5-turbo-1106", temperature=0.1):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]

def get_json_from_messages(messages, model="gpt-3.5-turbo-1106", temperature=0.1):
    response = openai.ChatCompletion.create(
        model=model,
        response_format={ "type": "json_object"},
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]

def get_gpt4v_response_from_image(image_url, question, model="gpt-4-vision-preview", max_tokens=300):
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": question},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]
        }
    ]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens
    )
    return response.choices[0].message["content"]


def get_gpt4v_response_from_encoded_image(base64_image, question, model="gpt-4-vision-preview"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": question
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()

def get_gpt4v_comparison_from_images(image_url1, image_url2, question, model="gpt-4-vision-preview"):
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": question,
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url1,
                    },
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url2,
                    },
                },
            ],
        }
    ]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=300,
    )
    return response.choices[0].message["content"]

def get_gpt4v_comparison_from_local_images(image_path1, image_path2, question, model="gpt-4-vision-preview"):
    base64_image1 = encode_image(image_path1)
    base64_image2 = encode_image(image_path2)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": question
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image1}"
                        }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image2}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 2000
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()

def main():
    # Get the current time
    start_time = time.time()
    print("Running...")

    # 入出力ファイル
    input_folder = "./data/"
    output_folder = "./output/"

    # query
    queries_path = "./prompt/queries.json"
    queries = read_json(queries_path)
    query1 = queries['query1']
    query2 = queries['query2']
    query3 = queries['query3']
    system_prompt = queries['system']
    query_json = read_file(queries['queryJsonResultFile'])

    print("=================================1.URL画像===============================")

    # 画像処理用のメッセージ
    # image_url = "https://imgproxy.snort.social/zWpNVNuWeW1c92fR27q5r2t8mwuecJmeeK_jM27sZUs//aHR0cHM6Ly92b2lkLmNhdC9kL1Vaam02NlY3dVRGdWJuRkMxM1RteGkud2VicA"
    # image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"

    # # 応答の取得
    # response1 = get_gpt4v_response_from_image(image_url, query1)
    # print(response1)

    print("=================================2.ローカル画像===============================")
    # ローカル画像に対して
    image_path = input_folder + "grape1.png"

    # Base64文字列の取得
    base64_image = encode_image(image_path)

    # 質問

    response2 = get_gpt4v_response_from_encoded_image(base64_image, query2)

    # 応答を表示
    print(response2)

    print("=================================3.二枚の画像の比較===============================")

    # 二枚の画像を比較
    # image_url1 = "https://imgproxy.snort.social/rNlL4GjXcH1LkFhCX7F_Y9FcV3emM_k-vP2ZskT9fvE//aHR0cHM6Ly92b2lkLmNhdC9kLzE2aTRnUTFlZmZ2U0pVNGR3ZGM3Yjcud2VicA"
    # image_url2 = "https://imgproxy.snort.social/aRCD9DTi_OalKR1bLZ8JStSWoXs9OSgNzg_7I1KH5HA//aHR0cHM6Ly92b2lkLmNhdC9kL1Jia3hyamhWOTFzUGs1a1B0U2NzcEQud2VicA"
    # image_url1 = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
    # image_url2 = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"

    # # 質問

    # response3 = get_gpt4v_comparison_from_images(image_url1, image_url2, query3)

    # # 応答を表示
    # print(response3)

    print("=================================3.二枚のローカル画像の比較===============================")

    image_path2 = input_folder + "grape2.png"
    image_path3 = input_folder + "grape3.png"
    response4 = get_gpt4v_comparison_from_local_images(image_path2, image_path3, query3)

    print(response4)

    print("=================================それぞれの解析結果===============================")
    print("########################### python jsonをリスト形式へ #####################################")



    # messages = []
    # messages.append({"role": "system", "content": system_prompt})
    # response = get_json_from_messages(messages)

    # print("=================================1のjson結果===============================")
    # messages.append({"role": "user", "content": query_json.format(result=response1)})
    # response = get_completion_from_messages(messages)
    # print("message:")
    # print(query_json.format(result=response1))
    # print("GPT:")
    # print(response)


    # print("=================================3のjson結果.2枚の比較===============================")
    # messages2 = []
    # messages2.append({"role": "system", "content": system_prompt})
    # response = get_json_from_messages(messages2)
    # messages2.append({"role": "user", "content": query_json.format(result=response3)})
    # response = get_completion_from_messages(messages2)
    # print("message:")
    # print(query_json.format(result=response3))
    # print("GPT:")
    # print(response)


    # try:
    #     data = json.loads(response)
    #     try:
    #         key_list = list(data["gpt4v-result"].keys())
    #         key_list_length = len(key_list)
    #         print("### 結果 ###")
    #         print(key_list)
    #         print("key_list_length:")
    #         print(key_list_length)
    #     except KeyError:
    #         return print("Error: 'gpt4v-result' key not found in the JSON data.")
    # except json.JSONDecodeError:
    #     return print("Error: Failed to decode JSON.")

    # Get the current time again
    end_time = time.time()

    # Compute the difference
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")

if __name__ == "__main__":
    main()