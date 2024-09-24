from gensim import corpora, models
import gensim
import pandas as pd

#모듈 (형태소분석기) 설치하기 
from konlpy.tag import Mecab
mecab = Mecab()


punct = "/-'?!.,#$%\'()*+-/:;<=>@[\\]^_`{|}~" + '""“”’' + '∞θ÷α•à−β∅³π‘₹´°£€\×™√²—–&'
punct_mapping = {"‘": "'", "₹": "e", "´": "'", "°": "", "€": "e", "™": "tm", "√": " sqrt ", "×": "x", "²": "2", "—": "-", "–": "-", "’": "'", "_": "-", "`": "'", '“': '"', '”': '"', '“': '"', "£": "e", '∞': 'infinity', 'θ': 'theta', '÷': '/', 'α': 'alpha', '•': '.', 'à': 'a', '−': '-', 'β': 'beta', '∅': '', '³': '3', 'π': 'pi', } 


def clean(text, punct, mapping):
    for p in mapping:
        text = text.replace(p, mapping[p])
    
    for p in punct:
        text = text.replace(p, f' {p} ')
    
    specials = {'\u200b': ' ', '…': ' ... ', '\ufeff': '', 'करना': '', 'है': ''}
    for s in specials:
        text = text.replace(s, specials[s])
    
    return text.strip()


import re


def clean_str(text):
    pattern = '([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)' # E-mail제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+' # URL제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '([ㄱ-ㅎㅏ-ㅣ]+)'  # 한글 자음, 모음 제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '<[^>]*>'         # HTML 태그 제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '[^\w\s\n]'         # 특수기호제거
    text = re.sub(pattern=pattern, repl='', string=text)
    text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]','', string=text)
    text = re.sub('\n', '.', string=text)
    return text 

#불용어 
#stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다', '것', '수', '일', '년', '국민', '등', '저', '말', '월', '저희', '후', '중', '내용', '시', '번', '만', '제', '명', '원','저', '상황', '차', '우리', '각', '원', '시간', '결과', '때문', '생각', '사람', '이상', '분', '때']

def text_preprocessing(text_list):
    #불용어 설정
    #stopwords = ['을', '를', '이', '가', '은', '는', 'null'] 
    stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다', '것', '국민', '등', '저', '말', '저희', '후', '중', '내용', '시', '번', '만', '제', '명', '원','저', '상황', '차', '우리', '각', '원', '시간', '결과', '때문', '생각', '사람', '이상', '분', '때', 'null']
    tokenizer = Meca() #형태소 분석기 
    token_list = []
    
    for text in text_list:
        txt = re.sub('[^가-힣a-z]', ' ', text) #한글과 소문자 외 제거
        token = tokenizer.morphs(txt) #tokenize (형태소 분석기)
        token = [t for t in token if t not in stopwords or type(t) != float] #불용어 제거 list
        token_list.append(token)
        
    return token_list, tokenizer

#형태소 분석기를 따로 저장한 이유는 후에 test 데이터 전처리를 진행할 때 이용해야 되기 때문입니다. 
#train['new_article'], okt = text_preprocessing(train['content']) 


'''
# 다른 노트북 파일에서 사용할 토큰 txt로 저장하기 
df_total_corpus=pd.DataFrame(tokenized_data)
columns=df_total_corpus.columns

df_total_corpus.fillna('', inplace=True)
df_total_corpus['total'] = df_total_corpus[columns].apply(' '.join, axis=1)

#txt로 한 문서를 한 줄씩 저장하기 
f = open("petition_tokens.txt", 'w')
for i in  range(len(df_total_corpus['total'])):
    data = df_total_corpus['total'].loc[i]
    f.write(data+'\n')
f.close()
'''

#tokenization
tokenized_data = []

for sentence in total_corpus:
    nouns_ele=mecab.nouns(sentence)
    nouns_removed= [word for word in nouns_ele if not word in stopwords] # 불용어 제거
    tokenized_data.append(nouns_removed)
    
#training vocabulary
dictionary = corpora.Dictionary(tokenized_data)

## 문서-단어 행렬(document-term matrix) 생성
corpus = [dictionary.doc2bow(term) for term in tokenized_data]

print(dictionary)

print(corpus)

model = models.ldamodel.LdaModel(corpus, num_topics=9, id2word = dictionary)
model.show_topics(4, 10)

NUM_TOPICS = 9

word_dict = {}
for i in range(NUM_TOPICS):
  words = model.show_topic(i, topn=20)
  word_dict['Topic #' + '{:02d}'.format(i+1)] = [i[0] for i in words]
  word_df = pd.DataFrame(word_dict)
  
model.print_topics(num_words=4)
model.get_document_topics(corpus)[0]

!pip install pyLDAvis  

import pyLDAvis
import pyLDAvis.gensim_models 

pyLDAvis.enable_notebook()

data = pyLDAvis.gensim_models.prepare(model, corpus, dictionary)
data