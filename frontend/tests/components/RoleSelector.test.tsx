import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { RoleSelector } from '@/components/RoleSelector';

describe('RoleSelector', () => {
  const mockOnSelect = jest.fn();

  beforeEach(() => {
    mockOnSelect.mockClear();
  });

  it('renders correctly', () => {
    render(<RoleSelector onSelect={mockOnSelect} />);
    expect(screen.getByText('Select Your Role')).toBeInTheDocument();
    expect(screen.getByText('Construction Worker')).toBeInTheDocument();
    expect(screen.getByText('Supplier / Subcontractor')).toBeInTheDocument();
    expect(screen.getByText('Project Manager / Admin')).toBeInTheDocument();
  });

  it('calls onSelect with correct role when Construction Worker is clicked', () => {
    render(<RoleSelector onSelect={mockOnSelect} />);
    fireEvent.click(screen.getByText('Construction Worker'));
    expect(mockOnSelect).toHaveBeenCalledWith('Construction Worker');
  });

  it('calls onSelect with correct role when Supplier is clicked', () => {
    render(<RoleSelector onSelect={mockOnSelect} />);
    fireEvent.click(screen.getByText('Supplier / Subcontractor'));
    expect(mockOnSelect).toHaveBeenCalledWith('Supplier / Subcontractor');
  });

  it('calls onSelect with correct role when Project Manager is clicked', () => {
    render(<RoleSelector onSelect={mockOnSelect} />);
    fireEvent.click(screen.getByText('Project Manager / Admin'));
    expect(mockOnSelect).toHaveBeenCalledWith('Project Manager / Admin');
  });
});
