import os
from openai import OpenAI

client = OpenAI()
client.organization='org-bViUymTUSW9oQ1iJBmC2xi8M' 
client.project="proj_05esYRj6UHC9Sn7Eq8twMrlS"

from openai import OpenAI
client = OpenAI()

"""
response = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
  ]
)
print(response)


response = client.embeddings.create(
    model="text-embedding-3-small",
    input="The food was delicious and the waiter..."
)
print(response)
"""


response = client.images.generate(
        prompt="A cute baby sea otter", 
        n=1, 
        size="1024x1024"
)
print(response)

# test upload / push 
