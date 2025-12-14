import React from 'react';
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import { Button } from '@/components/ui/button'; // Adjust path if necessary

expect.extend(toHaveNoViolations);

describe('Button Accessibility', () => {
  it('should have no accessibility violations', async () => {
    const { container } = render(<Button>Click me</Button>);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should have no accessibility violations when disabled', async () => {
    const { container } = render(<Button disabled>Click me</Button>);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should have no accessibility violations for different variants', async () => {
    const { container } = render(
      <div>
        <Button variant="default">Default</Button>
        <Button variant="destructive">Destructive</Button>
        <Button variant="outline">Outline</Button>
        <Button variant="secondary">Secondary</Button>
        <Button variant="ghost">Ghost</Button>
        <Button variant="link">Link</Button>
      </div>
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
