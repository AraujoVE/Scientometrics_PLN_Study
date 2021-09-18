import re
from num2words import num2words
import contractions
import string
import unicodedata
import os

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
#nltk.download('stopwords')
#nltk.download('punkt') 
#nltk.download('wordnet')




# convert text to ascii
def toAscii(text,convertToAscii=True):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8') if convertToAscii else text

# convert numbers to words
def processNumbers(text,removeNumbers):
    if removeNumbers:
        return re.sub(r'\d+', '', text)
    return re.sub(r'\d+', lambda n: num2words(int(n.group(0))), text)

# preprocess text
def preprocessText(text,removeNumbers=True,convertToAscii=True):
    text = text.lower() # lowercase text
    text = processNumbers(text,removeNumbers) # remove numbers or convert numbers to words
    text = toAscii(text) # convert to ascii
    text = text.strip() # remove leading and trailing whitespace
    text = text.translate(str.maketrans('', '', string.punctuation)) # remove punctuation
    text = contractions.fix(text) # replace contractions with their expanded forms
    text = re.sub(r'\s+', ' ', text) # replace multiple spaces with single space

    return text

# remove stop words
def removeStopWords(text): 
    text = text.split()
    stopwords = set(nltk.corpus.stopwords.words('english'))
    text = [w for w in text if not w in stopwords]
    text = ' '.join(text)
    return text

# lemmatize text
def lemmatizeText(text):
    lemmatizer = WordNetLemmatizer()
    text = word_tokenize(text)
    text = [lemmatizer.lemmatize(word) for word in text]
    text = ' '.join(text)

    return text

# normalize text
def normalizeText(text):
    text = preprocessText(text)
    text = removeStopWords(text)
    text = lemmatizeText(text)
    return text

# nomalize texts from a list of files in a directory
def normalizeDirFiles(dir):
    textFilesNames = os.listdir(dir)
    texts = {}
    for file in textFilesNames:
        with open(dir+'/'+file, 'r') as f:
            texts[file] = normalizeText(f.read())

    path = os.path.join(dir,'Normalized')
    os.mkdir(path)

    for file in textFilesNames:
        with open(path+'/'+file, 'w') as f:
            f.write(texts[file])

    return texts