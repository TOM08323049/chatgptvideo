import base64
import requests
import os
import openai

# 替换成你的OpenAI API密钥
api_key = "sk-ZQA0Ob"

#需要分析的图片路径，这里路径需要对应上一个视频逐帧图文件输出的路径
images_folder_path = "testvd/fruit"


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

image_files = [f for f in os.listdir(images_folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))]

text = '这是一个视频的逐帧图片，请综合一起分析这些图片（视频）的内容，并且把这个当做一个广告素材视频来分析，你现在是一个专业的游戏素材评测辅助人员，请帮忙针对附件的素材，按照以下规则xxx'


# text 是对应prompt内容
messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": f"{text}"}
        ]
    }
]

# 图片转为64编码并且加入列表内
for image_file in image_files:
    image_path = os.path.join(images_folder_path, image_file)
    base64_image = encode_image(image_path)
    messages[0]["content"].append({
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
        }
    })

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

payload = {
    "model": "gpt-4-vision-preview",
    "messages": messages,
    "max_tokens": 3000
}

#需要设置timeout时间，否则等待响应过短导致失败
response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload,timeout=180)

print(response.json())




