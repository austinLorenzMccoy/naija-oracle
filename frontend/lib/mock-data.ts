// Rich mock data used as the instant default on every page.
// Real API responses replace these when the backend is reachable.

export const MOCK_PERSONAS = [
  {
    id: '1',
    user_id: 'demo-user',
    name: 'Emeka O.',
    age_range: '25-34',
    city: 'Lagos',
    lga: 'Eti-Osa',
    primary_language: 'igbo',
    review_style: 'expressive',
    avg_rating: 4.2,
    sentiment_volatility: 'medium',
    categories_reviewed: ['tech_gadget', 'fintech', 'restaurant'],
    sample_reviews: [
      'The speed dey sharp sharp, but price high like NEPA restoring light.',
      'Everything set finish, clean design wey no go fall hand.',
    ],
    cultural_markers: ['sharp sharp', 'NEPA', 'fall hand'],
    pidgin_intensity: 0.82,
    voice_radar: { skepticism: 0.72, aspiration: 0.88, value: 0.76, sass: 0.68, loyalty: 0.64 },
    cultural_density: 88,
    status: 'active_oracle',
  },
  {
    id: '2',
    user_id: 'demo-user',
    name: 'Aisha H.',
    age_range: '25-34',
    city: 'Kano',
    lga: 'Tarauni',
    primary_language: 'hausa',
    review_style: 'analytical',
    avg_rating: 4.5,
    sentiment_volatility: 'low',
    categories_reviewed: ['fashion', 'beauty', 'food'],
    sample_reviews: ['Quality dey, but delivery timing needs discipline.'],
    cultural_markers: ['quality dey', 'timing'],
    pidgin_intensity: 0.55,
    voice_radar: { skepticism: 0.58, aspiration: 0.74, value: 0.82, sass: 0.42, loyalty: 0.79 },
    cultural_density: 86,
    status: 'active',
  },
  {
    id: '3',
    user_id: 'demo-user',
    name: 'Tunde B.',
    age_range: '18-24',
    city: 'Lagos',
    lga: 'Yaba',
    primary_language: 'yoruba',
    review_style: 'casual',
    avg_rating: 3.9,
    sentiment_volatility: 'high',
    categories_reviewed: ['tech_gadget', 'entertainment', 'fintech'],
    sample_reviews: ['App clean, but the onboarding stress no make sense.'],
    cultural_markers: ['no make sense', 'clean'],
    pidgin_intensity: 0.75,
    voice_radar: { skepticism: 0.8, aspiration: 0.66, value: 0.7, sass: 0.73, loyalty: 0.52 },
    cultural_density: 75,
    status: 'active',
  },
]

export const MOCK_PERSONA_BY_ID: Record<string, typeof MOCK_PERSONAS[0]> = {
  '1': MOCK_PERSONAS[0],
  '2': MOCK_PERSONAS[1],
  '3': MOCK_PERSONAS[2],
}

export const MOCK_STATS = {
  total_personas: 156,
  active_personas: 89,
  cities_covered: 12,
  languages_supported: 5,
  avg_cultural_density: 0.87,
}

export const MOCK_EVAL = {
  task_a: { bertscore_f1: 0.87, rouge_l: 0.41, rmse: 0.68, cvi_hit_rate: 0.74, human_eval_score: 4.2 },
  task_b: { ndcg_at_10: 0.89, hit_rate_at_5: 0.82, cold_start_ndcg: 0.76, contextual_relevance_human: 4.3 },
}

export const MOCK_SIMULATE_RESULT = {
  review_text: "E be like say this Zobo fine die o — the colour deep like Lagos twilight and the taste sharp sharp. The packaging dey show class but abeg, the price too high for ordinary market woman. I go manage sha, taste dey there. Four stars from me — if dem reduce price small, e go be five.",
  predicted_rating: 4,
  behavioural_fidelity_score: 0.84,
  voice_profile_used: { pidgin_intensity: 0.82 },
}

export const MOCK_RECOMMENDATIONS = [
  {
    item_id: 'rec_001',
    name: 'Yellow Chilli Restaurant',
    category: 'Nigerian Fine Dining',
    predicted_rating: 4.4,
    context_score: 0.91,
    location: 'Victoria Island, Lagos',
    price_tier: '₦₦₦',
    reasoning: 'Matches your "Owambe DJ" mood with high-energy evening service and live Afrobeats band on Fridays.',
  },
  {
    item_id: 'rec_002',
    name: 'Nok by Alara',
    category: 'African Fusion',
    predicted_rating: 4.9,
    context_score: 0.87,
    location: 'Victoria Island, Lagos',
    price_tier: '₦₦',
    reasoning: 'Creative fusion menu — the oxtail stew and jollof risotto consistently rank highest for celebratory occasions in your budget range.',
  },
  {
    item_id: 'rec_003',
    name: 'Aboki Suya Spot',
    category: 'Street Food',
    predicted_rating: 4.8,
    context_score: 0.83,
    location: 'Palmgrove, Lagos',
    price_tier: '₦',
    reasoning: 'Suya signal from your cold-start answers. Hausa mallam has been grilling on this corner 15 years — cultural authenticity score 94%.',
  },
]
