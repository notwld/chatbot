
import pickle
import json, random, nltk, numpy as np
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
with open(r"C:\Users\hp\Desktop\chatbot\intents.json",'r') as data:
  intents = json.load(data)



words = []
classes = []
documents = []
ignore = ["?"]


for intent in intents["intents"]:
  for pattern in intent["patterns"]:
    word = nltk.word_tokenize(pattern)
    words.extend(word)

    documents.append((word,intent["tag"]))
    if intent['tag'] not in classes:
      classes.append(intent['tag'])



words = [stemmer.stem(word.lower()) for word in words if word not in ignore]
words = sorted(list(set(words)))

classes = sorted(list(set(classes)))
pickle.dump({"words":words,"classes":classes},open(r"C:\Users\hp\Desktop\chatbot\training_data","wb"))



from keras.models import load_model
model = load_model(r"C:\Users\hp\Desktop\chatbot\model.pkl")

with open(r"C:\Users\hp\Desktop\chatbot\training_data","rb") as data:
  data = pickle.load(data)
  words = data["words"]
  classes = data["classes"]


with open(r"C:\Users\hp\Desktop\chatbot\intents.json",'r') as data:
  intents = json.load(data)

def cleanUp(sentence):
  sentence_words = nltk.word_tokenize(sentence)
  sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
  return sentence_words

def bow(sentence, words):
  sentence_words = cleanUp(sentence)
  bag = [0] * len(words)
  for s in sentence_words:
    for i,w in enumerate(words):
      if w==s:
        bag[i] = 1
  bag = np.array(bag)
  return (bag)

ERR_THRESHOLD = 0.30

def classify(sentence):
  bag = bow(sentence,words) # generating all the possibilties from a sentence
  result = model.predict(np.array([bag]))

  result = [[i,r] for i,r in enumerate(result[0])]
  result.sort(key=lambda x: x[1], reverse=True)

  result_li = []
  for res in result:
    if res[1] > ERR_THRESHOLD:
      result_li.append((classes[res[0]],res[1])) #intent and probability

  return result_li




def get_response(sentence):
  res = classify(sentence)
  if res:
    while res:
      for intent in intents["intents"]:
        if intent["tag"] == res[0][0]:
          return random.choice(intent["responses"])

      res.pop(0)


