import nltk
import pyperclip
nltk.download('punkt')
nltk.download('stopwords')
import string
from heapq import nlargest

# Chiedo all'utente di inserire il testo da riassumere
text = pyperclip.paste()

## Calcolo lunghezza desiderata per il riassunto
if text.count(". ") > 20:
    length = int(round(text.count(". ") / 4, 0))
else:
    length = 3

## Rimuovo tutta la punteggiatura dal testo inserito
nopuch =[char for char in text if char not in string.punctuation]
nopuch = "".join(nopuch)

## Divido il testo in parole e rimuovi le stopwords
processed_text = [word for word in nopuch.split() if word.lower() not in nltk.corpus.stopwords.words('english')]

## Creazione dizionario frequenza parola nel testo inserito
# Conterrà per ciascuna parola il numero di quante volte viene viualizzata
word_freq = {}
for word in processed_text:
    if word not in word_freq:
        word_freq[word] = 1
    else:
        word_freq[word] = word_freq[word] + 1

## Normalizzazione della frequenza in rapporto [0,1]
max_freq = max(word_freq.values())
for word in word_freq.keys():
    word_freq[word] = (word_freq[word]/max_freq)

## Core function del processo di riassunzione
# Identifica grazie al word_freq il punteggio e quindi le frasi più importanti e rilevanti
sent_list = nltk.sent_tokenize(text)
sent_score = {}
for sent in sent_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_freq.keys():
            if sent not in sent_score.keys():
                sent_score[sent] = word_freq[word]
            else:
                sent_score[sent] = sent_score[sent] + word_freq[word]

## Generazione riassunto basato su sent_score calcolato
length = min(length, len(sent_score)) 
summary_sents = nlargest(length, sent_score, key=sent_score.get)
summary = " ".join(summary_sents)
print(summary)
