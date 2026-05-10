#!/usr/bin/env python3
"""
Build Cultural Voice Index (CVI) for Nigerian linguistic patterns
Constructs a comprehensive index of Nigerian cultural markers, Pidgin phrases,
and linguistic patterns from curated sources and Groq-assisted expansion
"""

import csv
import json
import random
import argparse
from pathlib import Path
from typing import List, Dict, Any, Set
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to import Groq client
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    logging.warning("Groq library not available. Will use base CVI only.")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CVIBuilder:
    """Build Cultural Voice Index for Nigerian linguistic patterns"""
    
    def __init__(self, groq_api_key: str = None):
        self.groq_api_key = groq_api_key or os.getenv('GROQ_API_KEY')
        if GROQ_AVAILABLE and self.groq_api_key:
            self.client = Groq(api_key=self.groq_api_key)
            self.use_groq = True
        else:
            self.client = None
            self.use_groq = False
            logger.info("Using base CVI without Groq expansion")
    
    def build_cvi(self, output_path: Path, expand_with_groq: bool = True) -> None:
        """Build comprehensive CVI"""
        logger.info("Building Cultural Voice Index...")
        
        # Base CVI from curated sources
        base_cvi = self._get_base_cvi()
        
        # Expand with Groq if available
        if expand_with_groq and self.use_groq:
            logger.info("Expanding CVI with Groq...")
            expanded_cvi = self._expand_cvi_with_groq(base_cvi)
        else:
            expanded_cvi = base_cvi
        
        # Add linguistic analysis
        final_cvi = self._add_linguistic_analysis(expanded_cvi)
        
        # Save to CSV
        self._save_cvi_csv(final_cvi, output_path)
        
        # Also save as JSON for easier processing
        json_path = output_path.with_suffix('.json')
        self._save_cvi_json(final_cvi, json_path)
        
        logger.info(f"CVI built with {len(final_cvi)} entries")
        self._print_cvi_stats(final_cvi)
    
    def _get_base_cvi(self) -> List[Dict[str, Any]]:
        """Get base CVI from curated Nigerian linguistic sources"""
        
        base_entries = [
            # Core Pidgin expressions
            {
                "phrase": "Omo",
                "translation": "Oh my God / Wow",
                "category": "Exclamation",
                "tribe": "Universal",
                "pidgin_intensity": 0.9,
                "sentiment": "Neutral",
                "context": ["Surprise", "Excitement", "Shock"],
                "typical_rating": 4.0,
                "frequency": "High",
                "examples": ["Omo, this food sweet!", "Omo, see traffic!"]
            },
            {
                "phrase": "Na",
                "translation": "Is / It is",
                "category": "Copula",
                "tribe": "Universal",
                "pidgin_intensity": 0.8,
                "sentiment": "Neutral",
                "context": ["Identification", "Confirmation"],
                "typical_rating": 3.5,
                "frequency": "High",
                "examples": ["Na me do am", "Na true"]
            },
            {
                "phrase": "Wetin",
                "translation": "What",
                "category": "Question",
                "tribe": "Universal",
                "pidgin_intensity": 0.7,
                "sentiment": "Neutral",
                "context": ["Inquiry", "Confusion"],
                "typical_rating": 3.0,
                "frequency": "High",
                "examples": ["Wetin happen?", "Wetin you want?"]
            },
            {
                "phrase": "Sharp sharp",
                "translation": "Quickly / Immediately",
                "category": "Adverb",
                "tribe": "Universal",
                "pidgin_intensity": 0.8,
                "sentiment": "Positive",
                "context": ["Urgency", "Efficiency"],
                "typical_rating": 4.5,
                "frequency": "Medium",
                "examples": ["Come sharp sharp", "Finish am sharp sharp"]
            },
            {
                "phrase": "No be small tin",
                "translation": "Not a small thing / Significant",
                "category": "Expression",
                "tribe": "Universal",
                "pidgin_intensity": 0.9,
                "sentiment": "Mixed",
                "context": ["Emphasis", "Significance"],
                "typical_rating": 3.5,
                "frequency": "Medium",
                "examples": ["No be small tin to build house"]
            },
            {
                "phrase": "Shakara",
                "translation": "Show off / Pretend",
                "category": "Verb",
                "tribe": "Yoruba",
                "pidgin_intensity": 0.7,
                "sentiment": "Negative",
                "context": ["Criticism", "Behavior"],
                "typical_rating": 2.5,
                "frequency": "Medium",
                "examples": ["No dey shakara for me", "Too much shakara"]
            },
            {
                "phrase": "Abeg",
                "translation": "Please / I beg",
                "category": "Politeness",
                "tribe": "Universal",
                "pidgin_intensity": 0.6,
                "sentiment": "Neutral",
                "context": ["Request", "Appeal"],
                "typical_rating": 4.0,
                "frequency": "High",
                "examples": ["Abeg help me", "Abeg, wait small"]
            },
            {
                "phrase": "Wahala",
                "translation": "Problem / Trouble",
                "category": "Noun",
                "tribe": "Universal",
                "pidgin_intensity": 0.8,
                "sentiment": "Negative",
                "context": ["Complaint", "Difficulty"],
                "typical_rating": 2.0,
                "frequency": "High",
                "examples": ["Wahala dey", "No wahala"]
            },
            {
                "phrase": "Gbam",
                "translation": "Exactly / Absolutely",
                "category": "Agreement",
                "tribe": "Universal",
                "pidgin_intensity": 0.7,
                "sentiment": "Positive",
                "context": ["Confirmation", "Agreement"],
                "typical_rating": 4.5,
                "frequency": "Medium",
                "examples": ["Gbam! You talk true", "Na gbam"]
            },
            {
                "phrase": "Ehen",
                "translation": "Oh really / I see",
                "category": "Response",
                "tribe": "Universal",
                "pidgin_intensity": 0.6,
                "sentiment": "Neutral",
                "context": ["Understanding", "Realization"],
                "typical_rating": 3.5,
                "frequency": "Medium",
                "examples": ["Ehen, now I understand", "Ehen?"]
            },
            # Food-related expressions
            {
                "phrase": "Chop",
                "translation": "Eat",
                "category": "Verb",
                "tribe": "Universal",
                "pidgin_intensity": 0.8,
                "sentiment": "Positive",
                "context": ["Food", "Eating"],
                "typical_rating": 4.0,
                "frequency": "High",
                "examples": ["Make we chop", "Chop knacks"]
            },
            {
                "phrase": "Go dey",
                "translation": "It's okay / Alright",
                "category": "Agreement",
                "tribe": "Universal",
                "pidgin_intensity": 0.7,
                "sentiment": "Positive",
                "context": ["Acceptance", "Agreement"],
                "typical_rating": 4.0,
                "frequency": "Medium",
                "examples": ["Go dey", "Na go dey"]
            },
            # Tribal-specific expressions
            {
                "phrase": "Nwanne",
                "translation": "Sibling / Brother/Sister",
                "category": "Address",
                "tribe": "Igbo",
                "pidgin_intensity": 0.8,
                "sentiment": "Positive",
                "context": ["Familiarity", "Relationship"],
                "typical_rating": 4.5,
                "frequency": "Medium",
                "examples": ["Nwanne, how far?", "My nwanne"]
            },
            {
                "phrase": "Bros",
                "translation": "Brother / Friend",
                "category": "Address",
                "tribe": "Universal",
                "pidgin_intensity": 0.6,
                "sentiment": "Positive",
                "context": ["Friendship", "Informal"],
                "typical_rating": 4.0,
                "frequency": "High",
                "examples": ["Bros, abeg help me", "Hey bros"]
            },
            {
                "phrase": "My guy",
                "translation": "My friend / Buddy",
                "category": "Address",
                "tribe": "Universal",
                "pidgin_intensity": 0.5,
                "sentiment": "Positive",
                "context": ["Friendship", "Informal"],
                "typical_rating": 4.0,
                "frequency": "High",
                "examples": ["My guy, how you dey?", "My guy no worry"]
            }
        ]
        
        return base_entries
    
    def _expand_cvi_with_groq(self, base_cvi: List[Dict]) -> List[Dict]:
        """Expand CVI using Groq to generate additional Nigerian expressions"""
        
        expanded_entries = base_cvi.copy()
        
        # Categories to expand
        categories = [
            "Greetings and Farewells",
            "Food and Eating", 
            "Transportation",
            "Shopping and Money",
            "Relationships and Family",
            "Work and Business",
            "Technology and Social Media",
            "Weather and Environment",
            "Emotions and Feelings",
            "Time and Scheduling"
        ]
        
        for category in categories:
            try:
                new_entries = self._generate_category_entries(category)
                expanded_entries.extend(new_entries)
                logger.info(f"Added {len(new_entries)} entries for {category}")
            except Exception as e:
                logger.error(f"Error generating entries for {category}: {e}")
                continue
        
        return expanded_entries
    
    def _generate_category_entries(self, category: str) -> List[Dict[str, Any]]:
        """Generate CVI entries for a specific category using Groq"""
        
        prompt = f"""
Generate 5 authentic Nigerian Pidgin expressions for the category: {category}

For each expression, provide:
- The phrase itself
- English translation
- Which Nigerian tribe(s) commonly use it
- Pidgin intensity (0.1-1.0)
- Sentiment (Positive/Negative/Neutral)
- Context where it's used
- Typical rating this person would give (1-5)
- Frequency (Low/Medium/High)
- 2 example sentences

Format as JSON array like:
[
  {{
    "phrase": "expression",
    "translation": "english meaning",
    "category": "{category}",
    "tribe": "tribe name",
    "pidgin_intensity": 0.7,
    "sentiment": "Positive",
    "context": ["context1", "context2"],
    "typical_rating": 4.0,
    "frequency": "Medium",
    "examples": ["example1", "example2"]
  }}
]

Make them authentic and culturally specific to Nigeria.
"""
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=800
            )
            
            response_text = response.choices[0].message.content
            
            # Try to parse JSON
            import re
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error generating {category} entries: {e}")
            return []
    
    def _add_linguistic_analysis(self, cvi_entries: List[Dict]) -> List[Dict]:
        """Add linguistic analysis to CVI entries"""
        
        for entry in cvi_entries:
            # Add linguistic complexity score
            entry["linguistic_complexity"] = self._calculate_complexity(entry["phrase"])
            
            # Add cultural authenticity score
            entry["cultural_authenticity"] = self._calculate_authenticity(entry)
            
            # Add usage confidence
            entry["usage_confidence"] = random.uniform(0.7, 1.0)
            
            # Add grammatical category
            entry["grammatical_category"] = self._determine_grammatical_category(entry["phrase"])
        
        return cvi_entries
    
    def _calculate_complexity(self, phrase: str) -> float:
        """Calculate linguistic complexity score"""
        # Simple heuristic based on length and structure
        base_score = min(len(phrase.split()) / 3, 1.0)
        
        # Adjust for common patterns
        if any(word in phrase.lower() for word in ["na", "dey", "go", "come"]):
            base_score += 0.1
        
        return min(base_score, 1.0)
    
    def _calculate_authenticity(self, entry: Dict) -> float:
        """Calculate cultural authenticity score"""
        base_score = entry["pidgin_intensity"] * 0.6
        
        # Boost for tribe-specific entries
        if entry["tribe"] != "Universal":
            base_score += 0.2
        
        # Boost for high frequency
        if entry["frequency"] == "High":
            base_score += 0.2
        
        return min(base_score, 1.0)
    
    def _determine_grammatical_category(self, phrase: str) -> str:
        """Determine grammatical category of phrase"""
        phrase_lower = phrase.lower()
        
        if any(word in phrase_lower for word in ["na", "be", "is", "are"]):
            return "Copula"
        elif phrase_lower.endswith("?"):
            return "Question"
        elif any(word in phrase_lower for word in ["sharp", "quick", "fast"]):
            return "Adverb"
        elif any(word in phrase_lower for word in ["omo", "guy", "bros", "sis"]):
            return "Address"
        elif any(word in phrase_lower for word in ["chop", "eat", "drink"]):
            return "Verb"
        elif any(word in phrase_lower for word in ["wahala", "problem", "issue"]):
            return "Noun"
        else:
            return "Expression"
    
    def _save_cvi_csv(self, cvi_entries: List[Dict], output_path: Path) -> None:
        """Save CVI to CSV file"""
        
        fieldnames = [
            "phrase", "translation", "category", "tribe", "pidgin_intensity",
            "sentiment", "context", "typical_rating", "frequency", "examples",
            "linguistic_complexity", "cultural_authenticity", "usage_confidence",
            "grammatical_category"
        ]
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for entry in cvi_entries:
                # Convert lists to strings for CSV
                row = entry.copy()
                row["context"] = "; ".join(row["context"])
                row["examples"] = "; ".join(row["examples"])
                
                writer.writerow({field: row.get(field, "") for field in fieldnames})
    
    def _save_cvi_json(self, cvi_entries: List[Dict], output_path: Path) -> None:
        """Save CVI to JSON file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(cvi_entries, f, indent=2, ensure_ascii=False)
    
    def _print_cvi_stats(self, cvi_entries: List[Dict]) -> None:
        """Print CVI statistics"""
        
        # Category distribution
        categories = {}
        tribes = {}
        sentiments = {}
        
        for entry in cvi_entries:
            cat = entry["category"]
            tribe = entry["tribe"]
            sentiment = entry["sentiment"]
            
            categories[cat] = categories.get(cat, 0) + 1
            tribes[tribe] = tribes.get(tribe, 0) + 1
            sentiments[sentiment] = sentiments.get(sentiment, 0) + 1
        
        avg_pidgin = sum(e["pidgin_intensity"] for e in cvi_entries) / len(cvi_entries)
        avg_authenticity = sum(e["cultural_authenticity"] for e in cvi_entries) / len(cvi_entries)
        
        logger.info("CVI Statistics:")
        logger.info(f"Total entries: {len(cvi_entries)}")
        logger.info(f"Categories: {len(categories)}")
        logger.info(f"Tribes represented: {len(tribes)}")
        logger.info(f"Average Pidgin intensity: {avg_pidgin:.2f}")
        logger.info(f"Average cultural authenticity: {avg_authenticity:.2f}")
        
        logger.info("Top categories:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]:
            logger.info(f"  {cat}: {count}")
        
        # Save metrics
        metrics_path = Path('metrics/cvi_stats.json')
        metrics_path.parent.mkdir(parents=True, exist_ok=True)
        
        stats = {
            'total_entries': len(cvi_entries),
            'categories': len(categories),
            'tribes_represented': len(tribes),
            'avg_pidgin_intensity': avg_pidgin,
            'avg_cultural_authenticity': avg_authenticity,
            'top_categories': dict(sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5])
        }
        
        with open(metrics_path, 'w') as f:
            json.dump(stats, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Build Cultural Voice Index")
    parser.add_argument("--output", default="data/processed/cvi.csv", help="Output CSV file path")
    parser.add_argument("--no-groq", action="store_true", help="Skip Groq expansion")
    parser.add_argument("--groq-api-key", help="Groq API key (overrides environment variable)")
    
    args = parser.parse_args()
    
    builder = CVIBuilder(args.groq_api_key)
    output_path = Path(args.output)
    
    expand_with_groq = not args.no_groq
    builder.build_cvi(output_path, expand_with_groq)

if __name__ == "__main__":
    main()
