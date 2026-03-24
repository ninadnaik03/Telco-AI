from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from datasets import Dataset
import json


def load_data(path):
    with open(path, "r") as f:
        data = json.load(f)

    texts = []
    for item in data:
        text = f"""
Issue: {item['issue']}
Symptoms: {item['symptoms']}
Cause: {item['cause']}
Resolution: {item['resolution']}
"""
        texts.append(text)

    return Dataset.from_dict({"text": texts})


def main():
    print("🚀 Starting training pipeline...")

    model_name = "Qwen/Qwen2.5-0.5B-Instruct"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    dataset = load_data("data/telecom_knowledge.json")

    def tokenize(example):
        return tokenizer(
            example["text"],
            truncation=True,
            padding="max_length",
            max_length=256
        )

    tokenized = dataset.map(tokenize)

    training_args = TrainingArguments(
        output_dir="./models/fine_tuned",
        per_device_train_batch_size=2,
        num_train_epochs=1,
        logging_steps=10,
        save_steps=50
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized
    )

    trainer.train()

    print(" Training complete")


if __name__ == "__main__":
    main()
