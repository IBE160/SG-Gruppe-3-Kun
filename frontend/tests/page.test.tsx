import '@testing-library/jest-dom'
import { render, screen } from '@testing-library/react'
import Page from '../app/page'

describe('Page', () => {
  it('renders heading', () => {
    render(<Page />)
    const heading = screen.getByRole('heading', { level: 1 })
    expect(heading).toBeInTheDocument()
    expect(heading).toHaveTextContent('HMSREG Chatbot')
  })

  it('renders buttons', () => {
    render(<Page />)
    expect(screen.getByText('Primary Action')).toBeInTheDocument()
    expect(screen.getByText('Secondary Action')).toBeInTheDocument()
  })
})
