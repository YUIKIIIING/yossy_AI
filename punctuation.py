import spacy
#stanzaからspacyに変更

# spaCyモデルのロード（英語モデル）
nlp = spacy.load("en_core_web_sm")  # 英語モデル

def add_punctuation(text):
    if not text.strip():
        return text  # 空の入力に対処
    
    # テキストの解析
    doc = nlp(text)
    punctuated_sentences = []

    for sentence in doc.sents:
        # 文末のトークンを取得
        last_token = sentence[-1].text.lower()
        
        # 疑問文の判定
        if sentence.text.endswith("?") or last_token in ["what", "why", "how", "where", "when", "who"]:
            punctuated_sentences.append(sentence.text.strip() + "?")
        # 感嘆文の判定
        elif last_token in ["amazing", "great", "wow", "incredible", "awesome"]:
            punctuated_sentences.append(sentence.text.strip() + "!")
        # それ以外は句点を追加
        else:
            punctuated_sentences.append(sentence.text.strip() + ".")
    
    # 文単位で結合して句読点付きテキストを生成
    punctuated_text = " ".join(punctuated_sentences)
    return punctuated_text