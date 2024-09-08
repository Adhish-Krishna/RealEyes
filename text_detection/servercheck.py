import torch
from transformers import BertTokenizer, BertForSequenceClassification, BertConfig
from flask import Flask, request, jsonify
import time

app = Flask(__name__)

model_dir = './final_model' #model path
config = BertConfig.from_pretrained(model_dir + '/config.json')

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')


model = BertForSequenceClassification(config=config)

try:
    state_dict = torch.load(model_dir + '/model.safetensors', weights_only=True)
    model.load_state_dict(state_dict)
except Exception as e:
    print(f"Error loading model state dict: {e}")

device = torch.device("cpu")
model.to(device)


def process_texts(texts, tokenizer, model, device):
    start_time = time.time()


    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt", max_length=512)


    inputs = {key: val.to(device) for key, val in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits


        probabilities = torch.softmax(logits, dim=-1)


        confidence, predictions = torch.max(probabilities, dim=-1)

    end_time = time.time()
    print("Time taken:", end_time - start_time, "seconds")

    result = "Real" if predictions.item() == 0 else "Fake"
    confidence_score = confidence.item()
    return result, confidence_score

@app.route('/classify', methods=['POST'])
def classify_text():
    try:
        data = request.json
        user_input = data['text']


        result, confidence_score = process_texts([user_input], tokenizer, model, device)

        return jsonify({"result": result, "confidence": round(confidence_score, 2)})

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, port=8000)
