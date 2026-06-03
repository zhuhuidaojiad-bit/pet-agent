from groq import Groq

client = Groq(api_key="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")

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "你好，请用中文介绍一下你自己"}
    ]
)

print(response.choices[0].message.content)