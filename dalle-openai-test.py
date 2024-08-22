import os
from openai import OpenAI

client = OpenAI()
client.organization='org-bViUymTUSW9oQ1iJBmC2xi8M', 

response = client.embeddings.create(
    model="text-embedding-3-small",
    input="The food was delicious and the waiter..."
)
print("Embedding Test= ", response[0].embedding)

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
    ]
)
print("test_generation= ", completion.choices[0].message['contents'])


response = client.images.create(
        prompt="A cute baby sea otter", 
        n=1, 
        size="1024x1024"
)
print("Generate image= ",response['data'][0]['url'])


