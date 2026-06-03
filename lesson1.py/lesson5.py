from groq import Groq

# 把引号里换成你的 Groq API Key
client = Groq(api_key="你的Key粘贴在这里")

# 发消息给 AI
response = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {"role": "user", "content": "你好，请用中文介绍一下你自己"}
    ]
)

# 打印回复
print(response.choices[0].message.content)
