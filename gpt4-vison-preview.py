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

text = '这是一个视频的逐帧图片，请综合一起分析这些图片（视频）的内容，并且把这个当做一个广告素材视频来分析，你现在是一个专业的游戏素材评测辅助人员，请帮忙针对附件的素材，按照以下的规则选择最合适的素材标签;并且按照要求输出最合适的标签值;创意标签是一级标签，包含以下值:[展示向、玩法向、福利向、剧情向、拓圈向、题材向];二级标签从属一级标签，展示向的子标签包含:[角色展示、卡牌展示、龙魔展示、属性技能、场景展示、宠物展示、种族阵营、黑化魔化]; 玩法向的子标签包含:[抽卡，十连抽百连抽、千连抽、策略战斗、策略养成、宠物养成、放置挂机、BOSS战、藤爬塔.PVP剧场故事战斗、塔防、三消、回合制战斗、动作类、开放世界、横版闯关、宠物对战AR抓宠、捏脸玩法、休闲类]，福利向的子标签包含:[登录送、礼包码];剧情向的子标签包含:[互动剧情、真人情景剧、延展剧]，拓圈向的子标签包含: 梗图、软色情、蹭IP、音乐卡点，题材向的子标签包含: 新世界观、黑化世界观、神话、魔幻];现在根据素材，一级标签只能选择1个，作为输出的第一个值;所选的一级标签从属的二级标签选择1个，作为输出的第二个值;第三和第四个输出值，则从所有的二级标签中选择。'

#这是一个视频的逐帧图片，请综合一起分析这些图片（视频）的内容，并且把这个当做一个广告素材视频来分析，你现在是一个专业的游戏素材评测辅助人员，请帮忙针对附件的素材，按照以下的规则选择最合适的素材标签;并且按照要求输出最合适的标签值;创意标签是一级标签，包含以下值:[展示向、玩法向、福利向、剧情向、拓圈向、题材向];二级标签从属一级标签，展示向的子标签包含:[角色展示、卡牌展示、龙魔展示、属性技能、场景展示、宠物展示、种族阵营、黑化魔化]; 玩法向的子标签包含:[抽卡，十连抽百连抽、千连抽、策略战斗、策略养成、宠物养成、放置挂机、BOSS战、藤爬塔.PVP剧场故事战斗、塔防、三消、回合制战斗、动作类、开放世界、横版闯关、宠物对战AR抓宠、捏脸玩法、休闲类]，福利向的子标签包含:[登录送、礼包码];剧情向的子标签包含:[互动剧情、真人情景剧、延展剧]，拓圈向的子标签包含: 梗图、软色情、蹭IP、音乐卡点，题材向的子标签包含: 新世界观、黑化世界观、神话、魔幻];现在根据素材，一级标签只能选择1个，作为输出的第一个值;所选的一级标签从属的二级标签选择1个，作为输出的第二个值;第三和第四个输出值，则从所有的二级标签中选择。

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




