import os
import sys
import time
from process_datasets import DataProcess
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline


class ClinicalNER():
    
    def __init__(self, threshold=0.1) -> None:
        # BERT base NER
        bert_tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
        bert_model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
        self.pipe_bert_base_ner = pipeline("ner", model=bert_model, tokenizer=bert_tokenizer)
        self.threshold = threshold

        # Medical NER
        self.pipe_medical_ner = pipeline(
            "token-classification", model="Clinical-AI-Apollo/Medical-NER", aggregation_strategy="simple")

    def annotate(self, texts: list) -> list:

        for text in texts:
            
            # Annotate text.
            bert_base_ner_results = self.pipe_bert_base_ner(text)
            medical_ner_results = self.pipe_medical_ner(text)

            medical_ner_results = list(filter(lambda x: x['score'] > self.threshold, medical_ner_results))
            
            # Filter B-PER and I-PER tokens and join them into PERSON
            new_results = []
            for token in bert_base_ner_results:
                if token['score'] > self.threshold:
                    continue

                if token["entity"] == "B-PER" or token["entity"] == "I-PER":
                    # Merge with previous PERSON token if distance is small
                    if new_results and new_results[-1]["entity_group"] == "PERSON" and token["start"] - new_results[-1]["end"] < 2:
                        new_results[-1]["end"] = token["end"]
                        new_results[-1]["word"] = text[new_results[-1]["start"]:new_results[-1]["end"]]
                    else:
                        new_results.append({"entity_group": "PERSON", "score": token["score"], "word": token["word"],
                                            "start": token["start"], "end": token["end"]})
                elif token["entity"] == "B-LOC" or token["entity"] == "I-LOC":
                    # Merge with previous LOCATION token if distance is small
                    if new_results and new_results[-1]["entity_group"] == "LOCATION" and token["start"] - new_results[-1]["end"] < 2:
                        new_results[-1]["end"] = token["end"]
                        new_results[-1]["word"] = text[new_results[-1]["start"]:new_results[-1]["end"]]
                    else:
                        new_results.append({"entity_group": "LOCATION", "score": token["score"], "word": token["word"], "start": token["start"], "end": token["end"]})
        # Output
        new_results += medical_ner_results
        
        return new_results
    
    def evaluate(self, results, annotation):
        correct = 0
        all = len(annotation)

        for result in results:
            # Get start and end.
            key = f"{result['start']}-{result['end']}"
            if key in annotation:
                correct += 1
        acc = correct/all
        print(f"Result for intervals: {acc}")
        return acc


if __name__ == "__main__":
    
    cner = ClinicalNER(threshold=0.1)
    
    i2b2_path = '../datasets/i2b2/Track1-de-indentification/PHI/'
    datap = DataProcess('i2b2', i2b2_path)

    files_list = os.listdir(i2b2_path)
    
    acc_sum = 0
    total_files = len(files_list)
    total_time = 0

    for f in files_list:
        # Preprocess file.
        file_path = os.path.join(i2b2_path, f)
        datap.parse_i2b2(file_path)

        # Run NER over text.
        start_time = time.time()    
        results = cner.annotate([datap.text])
        elapsed = time.time() - start_time
        print("--- %s seconds ---" % (elapsed))
        total_time += elapsed

        # Evaluate annotation.
        partial_acc = cner.evaluate(results, datap.annotation)
        acc_sum += partial_acc
        
    final_acc = acc_sum/total_files
    print(f"Final accuracy for interval identification: {final_acc}")
    print("Final --- %s seconds ---" % (total_time))