args = arguments.get_args()

print(args.mode)

# Import training phrases csv file
import csv

csv_path = "/content/corpus.csv"

corpus = []

with open(csv_path, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        corpus.append({'text': row[0], 'dep': row[1], 
                        'des': row[2]})

# Delete csv header
corpus.pop(0)

import re

TRAIN_DATA = []

# Get start and end position of the token inside the text value
def get_position(text, token):
  for match in re.finditer(token, text):
    return (match.start(), match.end()) 

# Get entity format (START, END, LABEL)
def get_entity(text, token, label):
  start, end = get_position(text, token)
  return (start, end, label)

for sentence in corpus:
  text = sentence["text"]
  get_entity(text, sentence["des"], "DES")
  print(text, sentence["dep"], "DEP")
  get_entity(text, sentence["dep"], "DEP")
  # item => (TEXT AS A STRING, {“entities”: [(START, END, LABEL)]}) 
  item = (text, {"entities": [get_entity(text, sentence["dep"], "DEP"), get_entity(text, sentence["des"], "DES")]})
  TRAIN_DATA.append(item)

print(TRAIN_DATA)

from pathlib import Path

model = None
output_dir=Path("/content")
n_iter=100

import spacy

#load the model
if model is not None:
    nlp = spacy.load(model)  
    print("Loaded model '%s'" % model)
else:
    nlp = spacy.blank('fr')  
    print("Created blank 'fr' model")

#set up the pipeline

# create the built-in pipeline components and add them to the pipeline

# nlp.create_pipe works for built-ins that are registered with spaCy
if "ner" not in nlp.pipe_names:
  ner = nlp.create_pipe("ner")
  nlp.add_pipe(ner, last=True)
# otherwise, get it so we can add labels
else:
  ner = nlp.get_pipe("ner")
  
# add labels
for _, annotations in TRAIN_DATA:
  for ent in annotations.get("entities"):
    ner.add_label(ent[2])

# if 'ner' not in nlp.pipe_names:
#     ner = nlp.create_pipe('ner')
#     nlp.add_pipe(ner, last=True)
# else:
#     ner = nlp.get_pipe('ner')

from spacy.util import minibatch, compounding
import random

# get names of other pipes to disable them during training
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
with nlp.disable_pipes(*other_pipes):  # only train NER
  # reset and initialize the weights randomly – but only if we're
  # training a new model
  if model is None:
    nlp.begin_training()
    for itn in range(n_iter):
      random.shuffle(TRAIN_DATA)
      losses = {}
      # batch up the examples using spaCy's minibatch
      batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
      for batch in batches:
        texts, annotations = zip(*batch)
        nlp.update(
          texts,  # batch of texts
          annotations,  # batch of annotations
          drop=0.5,  # dropout - make it harder to memorise data
          losses=losses)
        print("Losses", losses)

 # test the trained model

 # IOB code of named entity tag. 3 means the token begins an entity, 2 means it
 # is outside an entity, 1 means it is inside an entity, and 0 means no entity 
 # tag is set.
 
for text, _ in TRAIN_DATA:
  doc = nlp(text)
  print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
  print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])

# This part will create a JSON from the sentence with destination and departure keys

import json

def create_dic(text):
  doc = nlp(text)
  dictionary = {}

  for ent in doc.ents:
    if ent.label_ == 'DEP':
      dictionary['dep'] = ent.text
    if ent.label_ == 'DES':
      dictionary['des'] = ent.text

  print(dictionary)
  return dictionary

def create_json(text):
  doc = nlp(text)
  dictionary = {}

  for ent in doc.ents:
    if ent.label_ == 'DEP':
      dictionary['dep'] = ent.text
    if ent.label_ == 'DES':
      dictionary['des'] = ent.text

  jsonString = json.dumps(dictionary, indent=4)
  print(jsonString)
  return jsonString

create_json('Je cherche un train depuis Bresl pour Dijon')

import difflib

def is_similar(first, second, ratio):
    return difflib.SequenceMatcher(None, first, second).ratio() > ratio

def compare_location_to_database(location, knowledge_base, ratio):

  result = []
  
  s = location.title()

  for c in knowledge_base: 
    if is_similar(s,c, ratio):
      result.append(c)

  return result

# Ratio to compare
ratio = 0.7

# Misspelled city name
city_name = 'Mans'

# knowledge base to search the correctly spelled city name
base = ['New York', 'Amsterdam', 'Barcelona', 'Berlin', 'Prague', 'Le Mans']

compare_location_to_database(city_name, base, ratio)

import csv
import pandas as pd

csv_path = "/content/fr.csv"

df = pd.read_csv(csv_path)  

df.head()

cities_name = df["city"]

cities_name.head()

# Try algo in a sample of cities

location = 'Renne'

correct = '' 

for x in range(0, 5):
  c = cities_name[x]
  if is_similar(location,c, 0.70):
      correct = c

print(correct)

locations = create_dic('Je veux un train pour Mans depuis Dujon')

departure = locations["dep"]

# Method to find the most accurate city name
def find_correct_location(entity):
  prob = compare_location_to_database(entity, cities_name, 0.7)

  if len(prob) == 0:
    return None
  else:
    ratios = []

    for c in prob: 
      ratio = difflib.SequenceMatcher(None, location, c).ratio()
      ratios.append(ratio)


    max_value = max(ratios)
    max_index = ratios.index(max_value)

    return prob[max_index]

print(find_correct_location(departure))
print(find_correct_location('gdsggsd'))