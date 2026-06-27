import { useState } from 'react'

interface Post {
  slug: string
  title: string
  description: string
  date: string
  readingTime: string
  tags: string[]
}

interface Props {
  posts: Post[]
}

export default function SearchableBlogList({ posts }: Props) {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedTag, setSelectedTag] = useState<string | null>(null)

  const allTags = [...new Set(posts.flatMap(post => post.tags))].sort()

  const filteredPosts = posts.filter(post => {
    const q = searchQuery.toLowerCase()
    const matchesSearch = q === '' ||
      post.title.toLowerCase().includes(q) ||
      post.description.toLowerCase().includes(q) ||
      post.tags.some(tag => tag.toLowerCase().includes(q))

    const matchesTag = selectedTag === null || post.tags.includes(selectedTag)

    return matchesSearch && matchesTag
  })

  return (
    <div>
      <div className="relative">
        <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          type="text"
          placeholder="Rechercher un article..."
          value={searchQuery}
          onChange={e => setSearchQuery(e.target.value)}
          className="w-full bg-surface-card border border-border rounded-card pl-10 pr-10 py-2.5 text-sm text-text-primary placeholder-text-muted focus:outline-none focus:border-accent-cyan/50 focus:ring-1 focus:ring-accent-cyan/20 transition-all"
        />
        {searchQuery && (
          <button
            onClick={() => setSearchQuery('')}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-text-muted hover:text-text-primary transition-colors"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
      </div>

      {allTags.length > 0 && (
        <div className="flex flex-wrap gap-2 mt-5">
          <button
            onClick={() => setSelectedTag(null)}
            className={`text-xs font-semibold px-3 py-1.5 rounded-pill border transition-all ${
              selectedTag === null
                ? 'bg-accent-cyan/10 border-accent-cyan/30 text-accent-cyan'
                : 'bg-transparent border-border text-text-muted hover:border-text-muted hover:text-text-secondary'
            }`}
          >
            Tous
          </button>
          {allTags.map(tag => (
            <button
              key={tag}
              onClick={() => setSelectedTag(tag === selectedTag ? null : tag)}
              className={`text-xs font-semibold px-3 py-1.5 rounded-pill border transition-all ${
                selectedTag === tag
                  ? 'bg-accent-cyan/10 border-accent-cyan/30 text-accent-cyan'
                  : 'bg-transparent border-border text-text-muted hover:border-text-muted hover:text-text-secondary'
              }`}
            >
              {tag}
            </button>
          ))}
        </div>
      )}

      <p className="text-xs text-text-muted mt-5">
        {filteredPosts.length} article{filteredPosts.length !== 1 ? 's' : ''}
        {searchQuery && ` pour "${searchQuery}"`}
        {selectedTag && ` dans ${selectedTag}`}
      </p>

      {filteredPosts.length > 0 ? (
        <div className="grid grid-cols-2 gap-4 mt-4">
          {filteredPosts.map(post => (
            <a
              key={post.slug}
              href={`/blog/${post.slug}`}
              className="block bg-surface-card rounded-card border border-border p-5 no-underline hover:border-border-hover hover:bg-surface-hover transition-all duration-200 group"
            >
              <div className="flex items-center gap-2 text-xs text-text-muted mb-2">
                <time dateTime={post.date}>{post.date}</time>
                <span>·</span>
                <span>{post.readingTime} min</span>
              </div>
              <h3 className="text-sm font-semibold text-text-primary group-hover:text-accent-cyan transition-colors">
                {post.title}
              </h3>
              <p className="text-xs text-text-muted mt-1.5 line-clamp-2">
                {post.description}
              </p>
              {post.tags.length > 0 && (
                <div className="flex flex-wrap gap-1.5 mt-3">
                  {post.tags.map(tag => (
                    <span
                      key={tag}
                      className="inline-block text-[10px] font-semibold px-2 py-0.5 rounded-pill border bg-accent-cyan/8 border-accent-cyan/20 text-accent-cyan"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              )}
            </a>
          ))}
        </div>
      ) : (
        <div className="text-center py-16">
          <p className="text-text-muted text-sm">Aucun article trouvé</p>
          <button
            onClick={() => { setSearchQuery(''); setSelectedTag(null) }}
            className="mt-3 text-xs text-accent-cyan hover:underline bg-transparent border-none cursor-pointer"
          >
            Réinitialiser les filtres
          </button>
        </div>
      )}
    </div>
  )
}
