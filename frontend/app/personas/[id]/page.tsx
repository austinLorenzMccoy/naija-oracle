import PersonaDetailClient from './PersonaDetailClient'

export function generateStaticParams() {
  return Array.from({ length: 15 }, (_, i) => ({ id: String(i + 1) }))
}

export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  return <PersonaDetailClient personaId={id} />
}
