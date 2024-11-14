import stanza
import re

def clean_text(text):
    # 特殊文字を削除
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text.strip()

# Stanzaの英語モデルをダウンロード
stanza.download('en')

# パイプラインの初期化（tokenize, mwt, pos, lemma, depparseプロセッサを使用）
nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma,depparse')

# 句読点を追加する関数
def add_punctuation(text):
    if not text.strip():
        return text  # 空の入力に対処

    # テキストの解析
    doc = nlp(text)
    
    # 文単位で結合して句読点付きテキストを生成
    punctuated_text = " ".join([sentence.text for sentence in doc.sentences])
    return punctuated_text
