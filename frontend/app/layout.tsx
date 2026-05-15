import type { Metadata } from 'next'
import { Analytics } from '@vercel/analytics/next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Naija Oracle - Consumer Insights',
  description: 'LLM agents that simulate Nigerian consumer voices and deliver hyper-personalized recommendations.',
  generator: 'v0.app',
  icons: {
    icon: '/logo.jpg',
    apple: '/logo.jpg',
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" className="dark">
      <body className="antialiased bg-oracle-void text-text-primary">
        {children}
        {process.env.NODE_ENV === 'production' && <Analytics />}
      </body>
    </html>
  )
}
