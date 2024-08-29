import os
from openai import OpenAI
from pathlib import Path

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

# voice generation : TTS & STT test


speech_file_path = Path(__file__).parent / "speech.mp3"
with client.audio.speech.with_streaming_response.create(
  model="tts-1",
  voice="alloy",  # alloy, echo, fable, onyx, nova, shimmer 
  input= " 요즘은 초등학교 고학년이 되면 대학 입시 준비를 한다. 중학교에서 부터 영재고, 과학고, 자사고 등 특목고를 지망하기 때문에 그렇다. 늦둥이로 둔 아들이 학교 친구들이 여러 명 영재고에 지원을 했다고 한다. 그런데 다들 떨어지고 한 명이 남았는데, 내일이 합격자 발표인데, 합격을 할지 물어 보았다. 아빠가 가끔 점을 보면서 사람들의 일을 맞추는 것이 신기해서 이기도 하겠지만, 자신도 특목고를 가고 싶어 하는데, 왠지 경쟁심리도 있었을 것이다." +  "내일 4시면 결과를 알려준다고 했다는데, 사실 생각해 보면 행정상으로는 이미 합격 여부는 판가름이 난 상태이다 단지 그 내용을 모르고 있는 것이다. 아빠의 능력을 검사하는 것이라 생각도 들어서 정단을 해 보았다. " + " 하필이며 절기가 바뀌고 월장이 바뀌는 날이다. 월장이 午將에서 巳將으로 바뀐다. 방송에서는 22일이 처서라고 했지만, 밤 11시 55분을 넘어서 절기가 바뀌기 때문에 정단을 하기 애매한 시간인 건 사실이다. 정단은 오장을 넘기지 않고 이루어 졌다. " +  " 갑진년 임신월 오장 기미일 자시이다. 아들 친구의 본명은 축토, 행년은 진토이다. " +  " ​갑인순 기미일 7국은 반음과이다. 반음의 공망은 변동이 멈추는 것이다. 과체가 반음과, 정관사, 팔전, 무친이다. 팔전법은 음일에 4과의 상신인 미토의 후삼위이 있는 글자이다. 여기서는 4과가 미토이니 천지반 미토부터 세어서 3번째인 사화가 발용한다.  음일의 중말전은 간상신이다. 양의 경우는 이와 정반대이다. 팔전법은 갑인, 정미, 기미, 경신일에만 구성이 되는 특이한 과이다. " +  " 시험 정단이니 중요한 것은 염막귀인, 주작이다. 기토의 낮밤 귀인은 자수와 신금이다. 둘다 과전에 없다. " +  " 다음으로 찾는 것이 주작인데, 과전의 승신들이 청룡, 천후, 현무 밖에 없다. " +  " 게다가 4과도 삼전도 모두 공망이다. 초전 사화는 역마인데 유일하게 공망이 아니다. 그래서 불행전자고초시가 된다. 그러나 4과가 공망이니 사실 무슨 일이 이루어 지겠는가? " +  " 이제 반전이 있다. " +  " 본명 축토로 인하여 사과와 중말전이 살아났다. 불행전이라는 것은 나아가지 못한다는 것인데 초전 사화 역마가 움직일 수 있게 된 것이다. 행년은 진토이다. 진토 상신에 술토 주작이 임했다. 이 걸로 합격은 따놓은 것이다. 진토와 술토는 힘이 세기 때문에 소송 정단에서 감옥을 의미한다. 그러나 힘이 세기 때문에 우두머리의 상이다. 평소 좋은 성적이고 이번에도 좋은 성적을 받은 것이다. 진토는 태상이 승했고 행년 승신인 술토에는 주작이 승했으니 합격하여 잔치를 열게 된다. " +  " 다음날 아들이 놀라면서 학교에서 전화했다. 합격했다고 어떻게 알았냐고. 이미 나와 있는 결과를 맞추는 것인데 육임이 못 보여 줄 것은 당연히 없다. 시험을 치기 전에도 합격 여부를 알 수 있는데.." + " 아들에게 그래서 너에게도 올해 주작이 들었으니 특목고 시험을 잘 준비하라고 했다. " +  " 아마도 친구의 합격이 나름 자극이 될 것 같다. ",
  response_format='aac' # opus, aac, flac, wav, pcm 
  # languages = Korean, Japan, Chinese
  ) as response:
    response.stream_to_file(speech_file_path)

# speech-to-text
"""
from openai import OpenAI
client = OpenAI()

audio_file= open("/path/to/file/audio.mp3", "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)
print(transcription.text)
"""

# image generation
"""
response = client.images.generate(
        prompt="A cute baby sea otter", 
        n=1, 
        size="1024x1024"
)
print(response)
"""
# test upload / push 
