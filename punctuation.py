import spacy

# spaCyモデルのキャッシュ
nlp = None

# モデルを初期化
def load_spacy_model():
    global nlp
    if nlp is None:
        print("Loading spaCy model...")
        nlp = spacy.load("en_core_web_sm")  # 小型の英語モデルをロード
    return nlp

# テキストを解析する際に使用
def process_text(text):
    nlp = load_spacy_model()  # モデルをロード（初回だけ）
    doc = nlp(text)
    return doc

# テキストに句読点を追加する関数
def add_punctuation(doc):
    # docがstr型の場合、解析してspaCyのDoc型に変換
    if isinstance(doc, str):
        nlp = load_spacy_model()
        doc = nlp(doc)

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
