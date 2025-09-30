import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { 
  Card, 
  CardHeader, 
  CardTitle, 
  CardDescription, 
  CardContent, 
  CardFooter 
} from '@/components/ui/card'

describe('Card Component', () => {
  it('renders card with all parts', () => {
    render(
      <Card>
        <CardHeader>
          <CardTitle>Test Title</CardTitle>
          <CardDescription>Test Description</CardDescription>
        </CardHeader>
        <CardContent>Test Content</CardContent>
        <CardFooter>Test Footer</CardFooter>
      </Card>
    )
    
    expect(screen.getByText('Test Title')).toBeInTheDocument()
    expect(screen.getByText('Test Description')).toBeInTheDocument()
    expect(screen.getByText('Test Content')).toBeInTheDocument()
    expect(screen.getByText('Test Footer')).toBeInTheDocument()
  })

  it('applies custom className to Card', () => {
    const { container } = render(
      <Card className="custom-class">Content</Card>
    )
    const card = container.querySelector('[data-slot="card"]')
    expect(card).toHaveClass('custom-class')
  })

  it('renders card with only content', () => {
    render(<Card>Simple Card</Card>)
    expect(screen.getByText('Simple Card')).toBeInTheDocument()
  })

  it('renders CardHeader with proper structure', () => {
    const { container } = render(
      <CardHeader>
        <CardTitle>Title</CardTitle>
      </CardHeader>
    )
    const header = container.querySelector('[data-slot="card-header"]')
    expect(header).toBeInTheDocument()
  })

  it('renders CardTitle with proper styling', () => {
    const { container } = render(<CardTitle>Card Title</CardTitle>)
    const title = container.querySelector('[data-slot="card-title"]')
    expect(title).toHaveClass('font-semibold')
  })

  it('renders CardDescription with muted text', () => {
    const { container } = render(
      <CardDescription>Description text</CardDescription>
    )
    const description = container.querySelector('[data-slot="card-description"]')
    expect(description).toHaveClass('text-muted-foreground')
  })
})
