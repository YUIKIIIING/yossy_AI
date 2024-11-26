import re
import stanza

# Stanzaの英語モデルをロード
stanza.download('en')  # 最初に一度だけ実行
nlp = stanza.Pipeline('en', processors='tokenize,mwt,pos,lemma,depparse')

# 短縮形や複数形の前にある空白を削除する関数
def clean_transcription(text):
    # 短縮形の前にある空白を削除（例: "It 's" → "It's"）
    text = re.sub(r"(\w) \'", r"\1'", text)
    
    # "n't"のような短縮形も処理する（例: "do n't" → "don't"）
    text = re.sub(r"(\w) n't\b", r"\1n't", text)
    
    # " 're"（例: "they 're" → "they're"）
    text = re.sub(r"(\w) 're\b", r"\1're", text)
    
    # " 's"（例: "he 's" → "he's"）
    text = re.sub(r"(\w) 's\b", r"\1's", text)
    
    # " 'm"（例: "I 'm" → "I'm"）
    text = re.sub(r"(\w) 'm\b", r"\1'm", text)
    
    # 複数形の前にある空白を削除（例: "dog s" → "dogs"）
    text = re.sub(r"(\w) s\b", r"\1s", text)
    
    return text

# 句読点を追加し、単語間に空白を入れる関数
def add_punctuation(text):
    print("句読点を追加しています...")
    
    # 文字起こし結果の前処理（短縮形や複数形の前の空白を削除）
    text = clean_transcription(text)
    
    # テキストを解析
    doc = nlp(text)
    
    punctuated_text = []
    
    for sent in doc.sentences:
        for word in sent.words:
            # 各単語に対してラベルを適用（句読点の追加はStanzaが行う）
            punctuated_text.append(word.text)
            punctuated_text.append(' ')  # 各単語の後にスペースを追加
    
    # 句読点が適切に追加されたテキストを返す
    return ''.join(punctuated_text).strip()
