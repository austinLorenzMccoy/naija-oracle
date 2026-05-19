'use client'

import { useEffect, useState } from 'react'
import { Volume2 } from 'lucide-react'
import { useVoice } from '@/lib/use-voice'

interface SpeakButtonProps {
  text: string
  pidginIntensity?: number
  className?: string
}

const WAVE_DELAYS = [0, 100, 200, 300]

export function SpeakButton({ text, pidginIntensity = 0.5, className = '' }: SpeakButtonProps) {
  const { speak, stop, speaking } = useVoice()
  const [supported, setSupported] = useState(false)

  useEffect(() => {
    setSupported('speechSynthesis' in window)
  }, [])

  if (!supported) return null

  return (
    <>
      <style>{`
        @keyframes voice-wave {
          0%, 100% { height: 3px; }
          50% { height: 13px; }
        }
      `}</style>
      <button
        type="button"
        onClick={() => (speaking ? stop() : speak(text, { pidginIntensity }))}
        title={speaking ? 'Stop' : 'Play review aloud'}
        className={`flex items-center gap-1.5 px-3 py-1.5 border rounded text-xs font-medium transition-colors shrink-0 ${
          speaking
            ? 'border-oracle-amber-500 text-oracle-amber-500 bg-oracle-amber-500/10'
            : 'border-oracle-ash text-text-secondary hover:border-oracle-amber-500 hover:text-oracle-amber-500'
        } ${className}`}
      >
        {speaking ? (
          <>
            <div className="flex items-end gap-0.5 h-4">
              {WAVE_DELAYS.map((delay) => (
                <div
                  key={delay}
                  style={{
                    width: '3px',
                    height: '3px',
                    backgroundColor: 'currentColor',
                    borderRadius: '1px',
                    animation: `voice-wave 0.7s ease-in-out ${delay}ms infinite`,
                  }}
                />
              ))}
            </div>
            <span>Stop</span>
          </>
        ) : (
          <>
            <Volume2 className="w-3.5 h-3.5" />
            <span>Play</span>
          </>
        )}
      </button>
    </>
  )
}
