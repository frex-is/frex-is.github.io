import { defineCollection, z } from 'astro:content'

const TableContentItem: z.ZodType = z.lazy(() => z.object({
    id: z.string(),
    label: z.string(),
    children: z.array(TableContentItem).optional(),
}))

const blog = defineCollection({
    type: 'content',
    schema: z.object({
        title: z.string(),
        description: z.string(),
        date: z.string(),
        readingTime: z.string(),
        tags: z.array(z.string()).optional(),
        tableOfContent: z.array(TableContentItem.optional()).default([]),
    }),
})

export const collections = {
    blog,
}