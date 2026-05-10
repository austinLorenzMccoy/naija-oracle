'use client';
import { useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Star, Heart, MapPin, Users, TrendingUp } from 'lucide-react';

interface ColdStartAnswer {
  food: string;
  entertainment: string;
  bank: string;
  transport: string;
  social: string;
}

interface Recommendation {
  id: string;
  name: string;
  category: string;
  rating: number;
  description: string;
  distance?: string;
  price?: string;
  confidence: number;
}

export default function ColdStartDemo() {
  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState<Partial<ColdStartAnswer>>({});
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const questions = [
    { 
      id: 'food', 
      q: 'What\'s your go-to street food?', 
      opts: ['Suya', 'Shawarma', 'Boli', 'Moi Moi'],
      icon: '🍢'
    },
    { 
      id: 'entertainment', 
      q: 'Weekend vibes: what\'s your move?', 
      opts: ['AMVCA Movies', 'BBNaija Drama', 'Live Concert', 'Gaming'],
      icon: '🎬'
    },
    { 
      id: 'bank', 
      q: 'Your trusted banking app?', 
      opts: ['GTB', 'Kuda', 'Opay', 'PalmPay'],
      icon: '🏦'
    },
    { 
      id: 'transport', 
      q: 'How do you move around Lagos?', 
      opts: ['Uber/Bolt', 'Danfo Bus', 'Keke Napep', 'Bike'],
      icon: '🚗'
    },
    { 
      id: 'social', 
      q: 'Your social media poison?', 
      opts: ['Twitter/X', 'Instagram', 'TikTok', 'WhatsApp'],
      icon: '📱'
    }
  ];

  const handleAnswer = (qid: keyof ColdStartAnswer, ans: string) => {
    const newAnswers = { ...answers, [qid]: ans };
    setAnswers(newAnswers);
    
    if (step < questions.length - 1) {
      setStep(step + 1);
    } else {
      fetchRecommendations(newAnswers as ColdStartAnswer);
    }
  };

  const fetchRecommendations = async (ans: ColdStartAnswer) => {
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/v1/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          cold_start_answers: ans,
          user_preferences: {
            categories: ['food', 'entertainment', 'shopping'],
            location: 'Lagos, Nigeria'
          }
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch recommendations');
      }

      const data = await response.json();
      setRecommendations(data.recommendations || []);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      // Show error state instead of mock data
      setRecommendations([]);
    } finally {
      setIsLoading(false);
    }
  };

  const resetDemo = () => {
    setStep(0);
    setAnswers({});
    setRecommendations([]);
  };

  if (recommendations.length > 0) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-orange-50 p-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              🎉 Your Personalized Recommendations
            </h1>
            <p className="text-lg text-gray-600">
              Based on your Nigerian lifestyle preferences
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            {recommendations.map((rec) => (
              <Card key={rec.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <div>
                      <CardTitle className="text-lg">{rec.name}</CardTitle>
                      <CardDescription>{rec.category}</CardDescription>
                    </div>
                    <Badge variant="secondary" className="ml-2">
                      {Math.round(rec.confidence * 100)}% match
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center mb-2">
                    <Star className="h-4 w-4 text-yellow-400 fill-current" />
                    <span className="ml-1 text-sm font-medium">{rec.rating}</span>
                    {rec.distance && (
                      <>
                        <MapPin className="h-4 w-4 text-gray-400 ml-4" />
                        <span className="ml-1 text-sm text-gray-600">{rec.distance}</span>
                      </>
                    )}
                  </div>
                  <p className="text-sm text-gray-600 mb-3">{rec.description}</p>
                  {rec.price && (
                    <Badge variant="outline" className="mb-3">
                      {rec.price}
                    </Badge>
                  )}
                  <Button className="w-full">View Details</Button>
                </CardContent>
              </Card>
            ))}
          </div>

          <div className="text-center space-y-4">
            <Button onClick={resetDemo} variant="outline" size="lg">
              Try Again
            </Button>
            <Link href="/dashboard">
              <Button variant="secondary" size="lg">
                Back to Dashboard
              </Button>
            </Link>
          </div>
        </div>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-orange-50 flex items-center justify-center">
        <Card className="w-96">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl">🔮 Finding Your Vibe...</CardTitle>
            <CardDescription>
              Analyzing your Nigerian preferences
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <Progress value={(step + 1) / questions.length * 100} className="w-full" />
            <p className="text-center text-sm text-gray-600">
              Processing your answers...
            </p>
          </CardContent>
        </Card>
      </div>
    );
  }

  const currentQ = questions[step];
  const progress = ((step + 1) / questions.length) * 100;

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-orange-50 p-8">
      <div className="max-w-2xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🇳🇬 Cold-Start Onboarding
          </h1>
          <p className="text-lg text-gray-600 mb-2">
            Help us understand your Nigerian lifestyle
          </p>
          <p className="text-sm text-gray-500">
            {step + 1} of {questions.length} questions
          </p>
        </div>

        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-3">
                <span className="text-3xl">{currentQ.icon}</span>
                <div>
                  <CardTitle className="text-xl">{currentQ.q}</CardTitle>
                  <CardDescription>
                    Choose the option that best represents you
                  </CardDescription>
                </div>
              </div>
            </div>
            <Progress value={progress} className="w-full" />
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 gap-3">
              {currentQ.opts.map((opt) => (
                <Button
                  key={opt}
                  onClick={() => handleAnswer(currentQ.id as keyof ColdStartAnswer, opt)}
                  variant="outline"
                  className="h-16 text-lg hover:bg-purple-50 hover:border-purple-300 transition-colors text-left justify-start px-6"
                >
                  {opt}
                </Button>
              ))}
            </div>
          </CardContent>
        </Card>

        <div className="text-center">
          <p className="text-sm text-gray-500">
            💡 Your answers help us create personalized recommendations that match your Nigerian lifestyle
          </p>
        </div>
      </div>
    </div>
  );
}
