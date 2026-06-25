export interface NavLink {
  label: string
  href: string
}

export const NAVIGATION = {
  links: [
    { label: 'Accueil', href: '/' },
    { label: 'Blog', href: '/blog' },
  ] satisfies NavLink[],
  social: [
    { label: 'GitHub', url: 'https://github.com/muller-j' },
  ],
}