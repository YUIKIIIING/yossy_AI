import stanza

# Stanzaの英語モデルをロード
stanza.download('en')  # 最初に一度だけ実行
nlp = stanza.Pipeline('en', processors='tokenize,mwt,pos,lemma,depparse')

def add_punctuation(text):
    # テキストを解析
    doc = nlp(text)
    
    punctuated_text = []
    
    for sent in doc.sentences:
        sentence_text = []
        
        for word in sent.words:
            # 各単語を文章に追加
            sentence_text.append(word.text)
        
        # 文の終わりにピリオドを追加（文末の空白を削除後）
        punctuated_sentence = ' '.join(sentence_text).strip()
        if punctuated_sentence and punctuated_sentence[-1] not in ['.', '?', '!']:
            punctuated_sentence += '.'  # 文章の最後にピリオドを追加
        
        # 完成した文を全体に追加
        punctuated_text.append(punctuated_sentence)
    
    # すべての文を結合して最終的な結果を返す
    return ' '.join(punctuated_text).strip()

