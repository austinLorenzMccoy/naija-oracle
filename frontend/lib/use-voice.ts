'use client'

import { useCallback, useEffect, useState } from 'react'

export function useVoice() {
  const [speaking, setSpeaking] = useState(false)

  const speak = useCallback((text: string, options?: { pidginIntensity?: number }) => {
    if (typeof window === 'undefined' || !('speechSynthesis' in window)) return
    window.speechSynthesis.cancel()
    const utterance = new SpeechSynthesisUtterance(text)
    const intensity = options?.pidginIntensity ?? 0.5
    // Higher pidgin intensity → faster, slightly higher pitch
    utterance.rate = 0.9 + intensity * 0.4
    utterance.pitch = 1.0 + intensity * 0.25
    utterance.lang = 'en-NG'
    utterance.onstart = () => setSpeaking(true)
    utterance.onend = () => setSpeaking(false)
    utterance.onerror = () => setSpeaking(false)
    window.speechSynthesis.speak(utterance)
  }, [])

  const stop = useCallback(() => {
    if (typeof window === 'undefined') return
    window.speechSynthesis.cancel()
    setSpeaking(false)
  }, [])

  useEffect(() => {
    return () => {
      if (typeof window !== 'undefined') window.speechSynthesis.cancel()
    }
  }, [])

  return { speak, stop, speaking }
}
