#!/usr/bin/env python3
"""
Generate synthetic Nigerian personas using Groq API
Creates realistic personas with cultural, linguistic, and demographic attributes
"""

import json
import random
import argparse
from pathlib import Path
from typing import List, Dict, Any
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
    logging.warning("Groq library not available. Will generate mock personas.")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NigerianPersonaGenerator:
    """Generate realistic Nigerian personas with cultural attributes"""
    
    def __init__(self, groq_api_key: str = None):
        self.groq_api_key = groq_api_key or os.getenv('GROQ_API_KEY')
        if GROQ_AVAILABLE and self.groq_api_key:
            self.client = Groq(api_key=self.groq_api_key)
            self.use_groq = True
        else:
            self.client = None
            self.use_groq = False
            logger.info("Using mock persona generation")
    
    def generate_personas(self, count: int = 500) -> List[Dict[str, Any]]:
        """Generate specified number of Nigerian personas"""
        logger.info(f"Generating {count} Nigerian personas...")
        
        personas = []
        for i in range(count):
            if self.use_groq:
                persona = self._generate_persona_with_groq(i)
            else:
                persona = self._generate_mock_persona(i)
            personas.append(persona)
        
        return personas
    
    def _generate_persona_with_groq(self, index: int) -> Dict[str, Any]:
        """Generate persona using Groq API"""
        prompt = self._create_persona_prompt()
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=500
            )
            
            # Parse the response to extract persona attributes
            persona_text = response.choices[0].message.content
            return self._parse_persona_response(persona_text, index)
            
        except Exception as e:
            logger.error(f"Error generating persona with Groq: {e}")
            return self._generate_mock_persona(index)
    
    def _create_persona_prompt(self) -> str:
        """Create prompt for Groq to generate Nigerian persona"""
        return """
Generate a realistic Nigerian persona with the following format:
{
  "name": "Full Nigerian name",
  "age_range": "25-34",
  "gender": "Male/Female",
  "city": "Major Nigerian city",
  "lga": "Local Government Area",
  "state": "State",
  "tribe": "Major Nigerian tribe",
  "occupation": "Realistic occupation",
  "education_level": "Education level",
  "income_bracket": "Low/Medium/High",
  "marital_status": "Single/Married/Divorced",
  "languages": ["English", "Yoruba/Igbo/Hausa", "Pidgin"],
  "pidgin_intensity": 0.7,
  "tech_savviness": 0.6,
  "social_media_usage": ["WhatsApp", "Facebook", "Twitter"],
  "shopping_preferences": ["Price conscious", "Quality focused"],
  "review_style": "Street Honest/Formal/Enthusiastic",
  "cultural_values": ["Family oriented", "Respect for elders"],
  "favorite_foods": ["Jollof rice", "Suya", "Pounded yam"],
  "entertainment_preferences": ["Nollywood movies", "Afrobeats", "Football"]
}

Make it realistic and culturally authentic. Use Nigerian names, cities, and cultural references.
"""
    
    def _parse_persona_response(self, response_text: str, index: int) -> Dict[str, Any]:
        """Parse Groq response into structured persona"""
        try:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                persona_data = json.loads(json_match.group())
            else:
                # Fallback to mock generation
                return self._generate_mock_persona(index)
            
            # Add required fields
            persona_data['persona_id'] = f'persona_{index:04d}'
            persona_data['generation_method'] = 'groq'
            
            return persona_data
            
        except Exception as e:
            logger.error(f"Error parsing persona response: {e}")
            return self._generate_mock_persona(index)
    
    def _generate_mock_persona(self, index: int) -> Dict[str, Any]:
        """Generate mock persona with realistic Nigerian attributes"""
        
        # Nigerian names by gender
        male_names = ["Chukwuemeka", "Adebayo", "Ibrahim", "Oluwaseun", "Emeka", 
                     "Tunde", "Chidi", "Ahmadu", "Femi", "Obinna"]
        female_names = ["Funke", "Chinaza", "Aisha", "Ngozi", "Bisi", 
                       "Ada", "Zainab", "Chioma", "Remi", "Blessing"]
        surnames = ["Okafor", "Abubakar", "Adebayo", "Eze", "Mohammed", 
                   "Ogunleye", "Yusuf", "Okonkwo", "Bello", "Nwankwo"]
        
        # Demographics
        gender = random.choice(["Male", "Female"])
        first_names = male_names if gender == "Male" else female_names
        name = f"{random.choice(first_names)} {random.choice(surnames)}"
        
        # Age ranges with realistic distribution
        age_ranges = ["18-24", "25-34", "35-44", "45-54", "55+"]
        age_weights = [0.2, 0.35, 0.25, 0.15, 0.05]
        age_range = random.choices(age_ranges, weights=age_weights)[0]
        
        # Cities and states
        cities_data = [
            ("Lagos", "Lagos", ["Ikeja", "Surulere", "Victoria Island", "Ikorodu"]),
            ("Abuja", "FCT", ["Garki", "Wuse", "Maitama", "Asokoro"]),
            ("Port Harcourt", "Rivers", ["Obio-Akpor", "Eleme", "Bonny"]),
            ("Kano", "Kano", ["Kano Municipal", "Nassarawa", "Fagge"]),
            ("Ibadan", "Oyo", ["Ibadan North", "Ibadan South", "Egbeda"])
        ]
        
        city, state, lgas = random.choice(cities_data)
        lga = random.choice(lgas)
        
        # Tribes with regional distribution
        tribes = {
            "Lagos": ["Yoruba"],
            "Abuja": ["Hausa", "Yoruba", "Igbo"],
            "Port Harcourt": ["Igbo", "Ijaw"],
            "Kano": ["Hausa", "Fulani"],
            "Ibadan": ["Yoruba"]
        }
        tribe = random.choice(tribes.get(city, ["Yoruba", "Igbo", "Hausa"]))
        
        # Languages based on tribe
        language_map = {
            "Yoruba": ["English", "Yoruba", "Pidgin"],
            "Igbo": ["English", "Igbo", "Pidgin"],
            "Hausa": ["English", "Hausa", "Pidgin"],
            "Ijaw": ["English", "Ijaw", "Pidgin"],
            "Fulani": ["English", "Hausa", "Fulfulde", "Pidgin"]
        }
        
        # Occupations
        occupations = ["Teacher", "Banker", "Entrepreneur", "Student", "Civil Servant",
                      "Engineer", "Doctor", "Trader", "IT Professional", "Sales Manager"]
        
        # Cultural attributes
        persona = {
            "persona_id": f"persona_{index:04d}",
            "name": name,
            "age_range": age_range,
            "gender": gender,
            "city": city,
            "lga": lga,
            "state": state,
            "tribe": tribe,
            "occupation": random.choice(occupations),
            "education_level": random.choice(["Secondary", "Bachelor's", "Master's", "PhD"]),
            "income_bracket": random.choices(["Low", "Medium", "High"], weights=[0.4, 0.4, 0.2])[0],
            "marital_status": random.choices(["Single", "Married", "Divorced"], weights=[0.4, 0.5, 0.1])[0],
            "languages": language_map.get(tribe, ["English", "Pidgin"]),
            "pidgin_intensity": round(random.uniform(0.3, 0.9), 2),
            "tech_savviness": round(random.uniform(0.2, 0.9), 2),
            "social_media_usage": random.sample(["WhatsApp", "Facebook", "Twitter", "Instagram", "TikTok"], k=2),
            "shopping_preferences": random.sample(["Price conscious", "Quality focused", "Brand loyal", "Convenience"], k=2),
            "review_style": random.choice(["Street Honest", "Formal", "Enthusiastic", "Critical"]),
            "cultural_values": random.sample(["Family oriented", "Respect for elders", "Religious", "Community focused"], k=2),
            "favorite_foods": random.sample(["Jollof rice", "Suya", "Pounded yam", "Egusi soup", "Amala"], k=3),
            "entertainment_preferences": random.sample(["Nollywood movies", "Afrobeats", "Football", "Comedy shows", "Traditional music"], k=2),
            "generation_method": "mock"
        }
        
        return persona

def save_personas(personas: List[Dict], output_path: Path) -> None:
    """Save personas to JSON file"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(personas, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Saved {len(personas)} personas to {output_path}")
    
    # Print statistics
    print_persona_stats(personas)

def print_persona_stats(personas: List[Dict]) -> None:
    """Print generation statistics"""
    cities = {}
    tribes = {}
    age_ranges = {}
    
    for persona in personas:
        cities[persona['city']] = cities.get(persona['city'], 0) + 1
        tribes[persona['tribe']] = tribes.get(persona['tribe'], 0) + 1
        age_ranges[persona['age_range']] = age_ranges.get(persona['age_range'], 0) + 1
    
    logger.info("Persona Generation Statistics:")
    logger.info(f"Cities: {dict(sorted(cities.items()))}")
    logger.info(f"Tribes: {dict(sorted(tribes.items()))}")
    logger.info(f"Age ranges: {dict(sorted(age_ranges.items()))}")
    
    avg_pidgin = sum(p['pidgin_intensity'] for p in personas) / len(personas)
    logger.info(f"Average Pidgin intensity: {avg_pidgin:.2f}")
    
    # Save metrics
    metrics_path = Path('metrics/persona_stats.json')
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    
    stats = {
        'total_personas': len(personas),
        'average_pidgin_intensity': avg_pidgin,
        'cities': cities,
        'tribes': tribes,
        'age_ranges': age_ranges,
        'generation_method': personas[0]['generation_method'] if personas else 'unknown'
    }
    
    with open(metrics_path, 'w') as f:
        json.dump(stats, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Generate synthetic Nigerian personas")
    parser.add_argument("--count", type=int, default=500, help="Number of personas to generate")
    parser.add_argument("--output", default="data/processed/personas.json", help="Output file path")
    parser.add_argument("--groq-api-key", help="Groq API key (overrides environment variable)")
    
    args = parser.parse_args()
    
    generator = NigerianPersonaGenerator(args.groq_api_key)
    personas = generator.generate_personas(args.count)
    
    output_path = Path(args.output)
    save_personas(personas, output_path)

if __name__ == "__main__":
    main()
