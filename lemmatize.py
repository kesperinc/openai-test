from konlpy.tag import Komoran
komoran=Komoran()

def lemmatize(sentence):
    morphtags = komoran.pos(sentence)
    words = []
    for m, t in enumerate(morphtags) :
      k = t.get_pos()
      if k=='NNP' or k=='NNG' :
        words.append(t.get_morph())
      elif k=='VA' or k=='VV' :
        words.append(t.get_morph()+'다')
    return words
print(komoran.morphs('안녕. 나는 하늘색과 딸기를 좋아해'))

sunstic = komoran.morphs('안녕. 나는 하늘색과 딸기를 좋아해')

w_ = []
for i in range(len(sunstic)) :
  words = lemmatize(sunstic.iloc[i]['review'])
  w_.append(' '.join(words))
df['words'] = w_  
df = df[df['words']!='']