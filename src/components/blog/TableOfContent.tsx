import { useEffect, useRef } from 'react'
import { useActiveHeading } from '@hooks/useActiveHeadings.ts'

interface TableContentItem {
  id: string
  label: string
  number?: string
  children?: TableContentItem[]
}

interface TableContentListProps {
  items: TableContentItem[]
  activeId?: string | null
  depth?: number
}

function TableContentList({
  items,
  activeId,
  depth = 1,
}: TableContentListProps) {
  return (
    <>
      {items.map((item) => (
        <div key={item.id}>
          <a
            href={`#${item.id}`}
            className={`
              block py-1 pr-0 no-underline transition-all duration-200
              border-l-2 border-transparent
              ${depth > 1 ? 'pl-6 text-[11px]' : 'pl-3 text-xs'}
              ${
                activeId === item.id
                  ? 'text-accent-cyan border-l-accent-cyan'
                  : 'text-text-subtle hover:text-text-muted'
              }
            `}
          >
            {item.number && (
              <span
                className="font-mono text-[10px] font-bold text-accent-cyan mr-1.5 px-1.5 py-0.5 rounded-pill border border-border/50 bg-surface/80"
              >
                {item.number}
              </span>
            )}

            {item.label}
          </a>

          {item.children && item.children.length > 0 && (
            <TableContentList
              items={item.children}
              activeId={activeId}
              depth={depth + 1}
            />
          )}
        </div>
      ))}
    </>
  )
}

export default function TableOfContent({
  items,
}: {
  items: TableContentItem[]
}) {
  const ids: string[] = []

  const collectIds = (nodes: TableContentItem[]) => {
    for (const node of nodes) {
      ids.push(node.id)

      if (node.children) {
        collectIds(node.children)
      }
    }
  }

  collectIds(items)

  const activeId = useActiveHeading(ids)
  const containerRef = useRef<HTMLElement>(null)

  // Keep the active entry centered in the TOC's own scroll area, without scrolling the page
  useEffect(() => {
    const container = containerRef.current
    if (!container || !activeId) return

    const link = container.querySelector<HTMLElement>(`a[href="#${CSS.escape(activeId)}"]`)
    if (!link) return

    const containerRect = container.getBoundingClientRect()
    const linkRect = link.getBoundingClientRect()
    const offset = linkRect.top - containerRect.top - (container.clientHeight - linkRect.height) / 2

    container.scrollBy({ top: offset, behavior: 'smooth' })
  }, [activeId])

  if (items.length === 0) return null

  return (
    <aside
      ref={containerRef}
      className="w-[240px] shrink-0 sticky top-20 h-fit max-h-[calc(100vh-120px)] overflow-y-auto px-4 py-6 border-l border-border hidden lg:block"
      aria-label="Table des matières"
    >
      <div className="text-[10px] uppercase tracking-widest text-text-subtle font-bold mb-4">
        Table des matières
      </div>

      <nav>
        <TableContentList
          items={items}
          activeId={activeId}
        />
      </nav>
    </aside>
  )
}