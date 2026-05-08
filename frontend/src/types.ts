export type View = 'dashboard' | 'simulator' | 'recommendations' | 'personas' | 'settings' | 'landing';

export interface Persona {
  id: string;
  name: string;
  tagline: string;
  role: string;
  location: string;
  lga: string;
  languages: string[];
  status: string;
  avatar: string;
  voiceRadar: {
    skepticism: number;
    aspiration: number;
    loyalty: number;
    value: number;
    sass: number;
  };
  culturalDensity: number;
}

export const PERSONAS: Persona[] = [
  {
    id: 'emeka',
    name: 'Emeka O.',
    tagline: 'Premium Tech Enthusiast',
    role: 'Trader, Alaba International',
    location: 'Lagos, NG',
    lga: 'Eti-Osa',
    languages: ['English', 'Igbo', 'Pidgin'],
    status: 'ACTIVE_ORACLE',
    avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDf_JseQ8MDFPYc0JelskXtJ2A9BxGesGu_vx673M9dNRj1Qa5MLEYYdVKTDXaNtrLlR04tD3rCazgByQ8Da3LGRGj9zsadoR3T1uKrFC6XBPMCZbH_4mOBpdbuZxO8CD9ROVpIGrH_2NhP9HFurYJAsXYKw_q9RHyhaCCyT2h9UksGI0jFawZzROGDzTuioSm8ZVL-4k1DSx-YN3o2qS9cp7LxWInOZrCFxreLOjEZmcHEP9ONxVJcO4HYogWi1gXmqbBDDXnaKiI',
    voiceRadar: { skepticism: 80, aspiration: 60, loyalty: 40, value: 90, sass: 50 },
    culturalDensity: 88,
  },
  {
    id: 'teniola',
    name: 'Teniola',
    tagline: 'The Tech-Baddie',
    role: 'Professional • Lekki Phase 1',
    location: 'Victoria Island, Lagos',
    lga: 'Iru/Victoria Island',
    languages: ['English', 'Pidgin'],
    status: 'ACTIVE_ORACLE',
    avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuAaGBjDhwPEoszalJsW9V3c620Phvl6RSgIvhyH-0ODtSECtvk56-B98RegWd-TRnwOmuAqzac3s9pQIUg8FB5tZSR-WD3vz8d41ikYH69M3koAjDjRH2oI6QEByUkWuKYQMW6sZqWhpSQGCqvIXEPeL_QYZcvlLo43TGrDyvx1VZDoA0oZ81arduHEazndjquyhyxbJaTl9SANlAk7fTNy77pNonQAnjNxuyqFJmByIEkERVjrEuE_EUqe970aAe2HHbN6oayxvaU',
    voiceRadar: { skepticism: 40, aspiration: 90, loyalty: 70, value: 50, sass: 80 },
    culturalDensity: 92,
  },
   {
    id: 'aisha',
    name: 'Aisha',
    tagline: 'The Modern Northern Creative',
    role: 'Freelancer, Kano City',
    location: 'Kano, NG',
    lga: 'Kano Municipal',
    languages: ['English', 'Hausa'],
    status: 'ACTIVE_ORACLE',
    avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCGbg8BfCir7w4rvg0l3P-rtIl-h2SJjsbwYrAD6PVqmzw3GSSRL61Biy6HB_kjwqjVzYpk1o1poq31qHLspESeHJUx_pB8fzo1-mwKTvVwtzp2wQnHaG48DEXHMOMc4aLkp_laOCzohAU_cv3aI2ufNc11d1EJ53X3PFbrgb1opdoL03qCpE8uYzfoGDGWOS7LI12e5H4oSFcn2538yVQGBRzYPCGu3A7qJP_0SrlNQbB1xT6mI0OWnYZ2Ozb_k0XTBwn80Uarf3A',
    voiceRadar: { skepticism: 70, aspiration: 80, loyalty: 90, value: 60, sass: 30 },
    culturalDensity: 85,
  }
];
