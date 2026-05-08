"""
Training script for Persona Simulator (Task A)
Fine-tunes LLM for authentic Nigerian review generation
"""

import os
import json
import argparse
from datetime import datetime
from typing import Dict, List, Any
import pandas as pd
import numpy as np
import torch
from transformers import (
    AutoTokenizer, AutoModelForCausalLM, 
    TrainingArguments, Trainer, DataCollatorForLanguageModeling
)
from datasets import Dataset, load_dataset
import mlflow
import mlflow.pytorch
from tqdm import tqdm

from app.config import settings
from app.services.cultural_voice_index import CulturalVoiceIndex

class PersonaSimulatorTrainer:
    """Trainer for Task A - Persona Simulator"""
    
    def __init__(self, model_name: str = "meta-llama/Llama-3.1-8B"):
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.cvi = CulturalVoiceIndex()
        
        # MLflow experiment
        self.experiment_name = "naija_oracle_task_a"
        mlflow.set_experiment(self.experiment_name)
    
    def load_model(self):
        """Load base model and tokenizer"""
        print(f"Loading model: {self.model_name}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True,
            padding_side="right"
        )
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )
        
        print("Model loaded successfully")
    
    def prepare_training_data(self, data_path: str) -> Dataset:
        """Prepare training data with Nigerian cultural context"""
        print("Preparing training data...")
        
        # Load or generate training data
        if os.path.exists(data_path):
            with open(data_path, 'r') as f:
                training_data = json.load(f)
        else:
            training_data = self._generate_synthetic_data()
            self._save_training_data(training_data, data_path)
        
        # Convert to HuggingFace Dataset
        dataset = Dataset.from_list(training_data)
        
        # Tokenize data
        def tokenize_function(examples):
            return self.tokenizer(
                examples["text"],
                truncation=True,
                max_length=512,
                padding="max_length",
                return_tensors="pt"
            )
        
        tokenized_dataset = dataset.map(tokenize_function, batched=True)
        
        print(f"Dataset prepared with {len(tokenized_dataset)} examples")
        return tokenized_dataset
    
    def _generate_synthetic_data(self) -> List[Dict[str, Any]]:
        """Generate synthetic Nigerian review data"""
        print("Generating synthetic training data...")
        
        # Persona templates
        personas = [
            {
                "name": "Emeka O.",
                "city": "Lagos",
                "lga": "Surulere",
                "language": "Igbo",
                "pidgin_intensity": 0.7,
                "style": "expressive"
            },
            {
                "name": "Aisha",
                "city": "Kano",
                "lga": "Kano Municipal",
                "language": "Hausa",
                "pidgin_intensity": 0.3,
                "style": "formal"
            },
            {
                "name": "Tunde",
                "city": "Lagos",
                "lga": "Ikeja",
                "language": "Yoruba",
                "pidgin_intensity": 0.8,
                "style": "casual"
            }
        ]
        
        # Product templates
        products = [
            {"name": "Chicken Republic", "category": "fast_food", "location": "Ikeja"},
            {"name": "Yellow Chilli", "category": "restaurant", "location": "Victoria Island"},
            {"name": "Jumia Food", "category": "delivery", "location": "Online"},
            {"name": "Shoprite", "category": "grocery", "location": "Lekki"},
            {"name": "Silverbird Cinema", "category": "entertainment", "location": "Ikeja City Mall"}
        ]
        
        # CVI anchors for cultural authenticity
        cvi_phrases = [
            "E sweet me die", "Wahala be like bicycle", "E dey manage",
            "Dem cheat me", "The vibe no catch me", "Gbam!", "E go be",
            "Orente", "Nwoke oma", "Lafiya", "Cost like madness",
            "Slow like NEPA", "Correct!"
        ]
        
        training_examples = []
        
        for persona in personas:
            for product in products:
                for rating in [1, 2, 3, 4, 5]:
                    # Generate review based on persona and rating
                    review = self._generate_review(
                        persona, product, rating, cvi_phrases
                    )
                    
                    # Create training prompt
                    prompt = self._create_training_prompt(persona, product, review)
                    
                    training_examples.append({
                        "text": prompt,
                        "persona": persona,
                        "product": product,
                        "rating": rating,
                        "review": review
                    })
        
        return training_examples
    
    def _generate_review(self, persona: Dict, product: Dict, rating: int, cvi_phrases: List[str]) -> str:
        """Generate authentic Nigerian review"""
        
        # Select CVI phrases based on persona and rating
        if rating >= 4:
            positive_phrases = [p for p in cvi_phrases if any(word in p for word in ["sweet", "correct", "gbam", "orente", "lafiya"])]
            anchor = np.random.choice(positive_phrases) if positive_phrases else "Correct!"
        elif rating <= 2:
            negative_phrases = [p for p in cvi_phrases if any(word in p for word in ["wahala", "cheat", "cost", "slow"])]
            anchor = np.random.choice(negative_phrases) if negative_phrases else "E dey manage"
        else:
            anchor = np.random.choice(cvi_phrases)
        
        # Generate review based on persona characteristics
        if persona["pidgin_intensity"] > 0.6:
            # High pidgin
            if rating >= 4:
                return f"This {product['name']} for {product['location']}, {anchor}! The service correct, I go come back for sure. 5 stars!"
            elif rating <= 2:
                return f"This {product['name']} {anchor}. Service slow like NEPA and price cost like madness. No recommend."
            else:
                return f"This {product['name']} e dey manage. Not bad but not great either. {product['location']} branch need improvement."
        else:
            # Lower pidgin, more formal
            if rating >= 4:
                return f"The {product['name']} at {product['location']} was excellent. Great service and quality. Highly recommended."
            elif rating <= 2:
                return f"I was disappointed with {product['name']} at {product['location']}. Poor service and overpriced."
            else:
                return f"The {product['name']} at {product['location']} was average. Some good aspects but needs improvement."
    
    def _create_training_prompt(self, persona: Dict, product: Dict, review: str) -> str:
        """Create training prompt with persona context"""
        
        prompt = f"""<s>[INST]
You are Naija Oracle — a cultural intelligence system that generates authentic Nigerian consumer reviews.

PERSONA:
- Name: {persona['name']}
- City: {persona['city']} | LGA: {persona['lga']}
- Language: {persona['language']} | Pidgin intensity: {persona['pidgin_intensity']:.1f}/1.0
- Style: {persona['style']}

PRODUCT TO REVIEW:
- Name: {product['name']}
- Category: {product['category']}
- Location: {product['location']}

Generate an authentic review that sounds exactly like this persona would write it.
[/INST]

{review}</s>"""
        
        return prompt
    
    def _save_training_data(self, data: List[Dict], path: str):
        """Save training data to file"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Training data saved to {path}")
    
    def train_model(self, dataset: Dataset, output_dir: str, num_epochs: int = 3):
        """Fine-tune the model"""
        print("Starting model training...")
        
        # Split dataset
        train_test_split = dataset.train_test_split(test_size=0.1, seed=42)
        train_dataset = train_test_split["train"]
        eval_dataset = train_test_split["test"]
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=num_epochs,
            per_device_train_batch_size=4,
            per_device_eval_batch_size=4,
            gradient_accumulation_steps=4,
            warmup_steps=100,
            logging_steps=10,
            evaluation_strategy="steps",
            eval_steps=100,
            save_steps=500,
            learning_rate=2e-5,
            weight_decay=0.01,
            fp16=True,
            dataloader_pin_memory=False,
            gradient_checkpointing=True,
            save_total_limit=3,
            load_best_model_at_end=True,
            metric_for_best_model="eval_loss",
            greater_is_better=False,
            report_to="mlflow"
        )
        
        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )
        
        # Trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            data_collator=data_collator,
            tokenizer=self.tokenizer
        )
        
        # Start training with MLflow logging
        with mlflow.start_run(run_name=f"persona_simulator_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
            # Log parameters
            mlflow.log_params({
                "model_name": self.model_name,
                "num_epochs": num_epochs,
                "learning_rate": 2e-5,
                "batch_size": 4,
                "dataset_size": len(train_dataset)
            })
            
            # Train model
            trainer.train()
            
            # Evaluate model
            eval_results = trainer.evaluate()
            
            # Log metrics
            mlflow.log_metrics({
                "eval_loss": eval_results["eval_loss"],
                "perplexity": np.exp(eval_results["eval_loss"])
            })
            
            # Save model
            trainer.save_model(output_dir)
            self.tokenizer.save_pretrained(output_dir)
            
            # Log model to MLflow
            mlflow.pytorch.log_model(
                self.model,
                "model",
                registered_model_name="naija_oracle_persona_simulator"
            )
            
            print(f"Training completed. Model saved to {output_dir}")
            print(f"Evaluation loss: {eval_results['eval_loss']:.4f}")
    
    def evaluate_model(self, model_path: str, test_data_path: str):
        """Evaluate trained model on test data"""
        print("Evaluating model...")
        
        # Load trained model
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        
        # Load test data
        with open(test_data_path, 'r') as f:
            test_data = json.load(f)
        
        # Generate predictions and calculate metrics
        from bert_score import score as bert_score
        from rouge_score import rouge_scorer
        
        rouge_scorer_obj = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
        
        bert_scores = []
        rouge_scores = []
        
        for example in tqdm(test_data[:100]):  # Evaluate on first 100 examples
            # Generate prediction
            prompt = example["text"].split("[/INST]")[0] + "[/INST]\n"
            inputs = self.tokenizer(prompt, return_tensors="pt").to(model.device)
            
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=100,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            prediction = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            prediction = prediction.split("[/INST]")[-1].strip()
            
            # Calculate metrics
            reference = example["review"]
            
            # BERTScore
            P, R, F1 = bert_score([prediction], [reference], lang="en")
            bert_scores.append(F1.item())
            
            # ROUGE-L
            rouge_score = rouge_scorer_obj.score(prediction, reference)
            rouge_scores.append(rouge_score["rougeL"].fmeasure)
        
        # Calculate averages
        avg_bert_score = np.mean(bert_scores)
        avg_rouge_score = np.mean(rouge_scores)
        
        # Log to MLflow
        mlflow.log_metrics({
            "avg_bert_score": avg_bert_score,
            "avg_rouge_l": avg_rouge_score
        })
        
        print(f"Evaluation Results:")
        print(f"Average BERTScore: {avg_bert_score:.4f}")
        print(f"Average ROUGE-L: {avg_rouge_score:.4f}")
        
        return {
            "bert_score": avg_bert_score,
            "rouge_l": avg_rouge_score
        }

def main():
    parser = argparse.ArgumentParser(description="Train Persona Simulator")
    parser.add_argument("--model", type=str, default="meta-llama/Llama-3.1-8B", help="Base model name")
    parser.add_argument("--data", type=str, default="data/persona_training_data.json", help="Training data path")
    parser.add_argument("--output", type=str, default="models/persona_simulator", help="Output directory")
    parser.add_argument("--epochs", type=int, default=3, help="Number of training epochs")
    parser.add_argument("--eval-only", action="store_true", help="Only run evaluation")
    
    args = parser.parse_args()
    
    trainer = PersonaSimulatorTrainer(args.model)
    
    if args.eval_only:
        # Load model for evaluation
        trainer.load_model()
        trainer.evaluate_model(args.output, args.data)
    else:
        # Full training pipeline
        trainer.load_model()
        dataset = trainer.prepare_training_data(args.data)
        trainer.train_model(dataset, args.output, args.epochs)
        
        # Evaluate after training
        trainer.evaluate_model(args.output, args.data)

if __name__ == "__main__":
    main()
