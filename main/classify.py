import torch
from torch import nn
import pandas as pd
from transformers import BertForSequenceClassification, BertTokenizer

if torch.cuda.is_available():    
    # Tell PyTorch to use the GPU.    
    device = torch.device("cuda")
# If not...
else:
    device = torch.device("cpu")

def getPrediction(tweet):
    tokenizer = BertTokenizer.from_pretrained("Hate-speech-CNERG/bert-base-uncased-hatexplain")
    model = BertForSequenceClassification.from_pretrained("Hate-speech-CNERG/bert-base-uncased-hatexplain")
    model = model.to(device)
    inputs = tokenizer(tweet, return_tensors="pt")
    outputs = model(**inputs)
    label = torch.argmax(torch.nn.functional.softmax(outputs.logits,dim=1))
    if (label == 0):
        return "hate-speech"
    elif (label == 2):
        return "offensive"
    return "normal"


