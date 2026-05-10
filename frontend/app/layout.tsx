import type { Metadata } from 'next'
import { DM_Sans, Fraunces, JetBrains_Mono } from 'next/font/google'
import { Analytics } from '@vercel/analytics/next'
import './globals.css'

const dmSans = DM_Sans({ subsets: ["latin"], weight: ["300", "400", "500", "700"] })
const fraunces = Fraunces({ subsets: ["latin"], weight: ["300", "700"] })
const jetBrainsMono = JetBrains_Mono({ subsets: ["latin"], weight: ["400", "500"] })

export const metadata: Metadata = {
  title: 'Naija Oracle - Consumer Insights',
  description: 'LLM agents that simulate Nigerian consumer voices and deliver hyper-personalized recommendations.',
  generator: 'v0.app',
  icons: {
    icon: [
      {
        url: '/icon-light-32x32.png',
        media: '(prefers-color-scheme: light)',
      },
      {
        url: '/icon-dark-32x32.png',
        media: '(prefers-color-scheme: dark)',
      },
      {
        url: '/icon.svg',
        type: 'image/svg+xml',
      },
    ],
    apple: '/apple-icon.png',
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${dmSans.className} antialiased bg-oracle-void text-text-primary`} style={{
        '--font-heading': fraunces.style.fontFamily,
        '--font-body': dmSans.style.fontFamily,
        '--font-mono-data': jetBrainsMono.style.fontFamily,
      } as React.CSSProperties}>
        {children}
        {process.env.NODE_ENV === 'production' && <Analytics />}
      </body>
    </html>
  )
}
