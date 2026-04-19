import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'GovScheme AI | Get Your Benefits',
  description: 'AI-Powered Government Scheme Recommendation Platform',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-800 text-slate-100 antialiased`}>
        {children}
      </body>
    </html>
  )
}
