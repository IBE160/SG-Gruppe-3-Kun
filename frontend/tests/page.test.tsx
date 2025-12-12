import '@testing-library/jest-dom'
import { render, screen, fireEvent, within } from '@testing-library/react'
import Page from '../app/page'

// Mock ChatWindow
jest.mock('@/components/ChatWindow', () => ({
  ChatWindow: ({ className, userRole }: { className?: string; userRole: string | null }) => ( // Added userRole
    <div data-testid="chat-window" className={className}>
      Chat Window Content for role: {userRole} {/* Display userRole in mock for verification */}
    </div>
  )
}));

// Mock RoleSelector
jest.mock('@/components/RoleSelector', () => ({
  RoleSelector: ({ onSelect }: { onSelect: (role: string) => void }) => (
    <button onClick={() => onSelect('Construction Worker')}>Select Construction Worker</button>
  )
}));

describe('Page Layout', () => {
  it('renders initial role selection screen', () => {
    render(<Page />)
    expect(screen.getByRole('heading', { level: 1, name: /HMSREG Documentation/i })).toBeInTheDocument()
    expect(screen.getByText('Select your role to get started')).toBeInTheDocument()
    expect(screen.queryByTestId('chat-window')).not.toBeInTheDocument()
    expect(screen.queryByTestId('mobile-view')).not.toBeInTheDocument()
    expect(screen.queryByTestId('desktop-view')).not.toBeInTheDocument()
  })

  it('renders responsive layout structure after role selection', () => {
    render(<Page />)
    const selectedRole = 'Construction Worker';
    fireEvent.click(screen.getByText('Select Construction Worker'));
    
    // Get the mobile and desktop views
    const mobileView = screen.getByTestId('mobile-view');
    const desktopView = screen.getByTestId('desktop-view');

    // Assert that the ChatWindow (mocked) is rendered within both,
    // and contains the correct role-specific text.
    // Use getAllByText as there will be two instances.
    const chatWindowsWithRoleText = screen.getAllByText(`Chat Window Content for role: ${selectedRole}`);
    expect(chatWindowsWithRoleText.length).toBe(2); // Expect two instances (one in each hidden/shown view)

    // Verify mobile view's ChatWindow
    expect(within(mobileView).getByText(`Chat Window Content for role: ${selectedRole}`)).toBeInTheDocument();
    // Verify desktop view's ChatWindow
    expect(within(desktopView).getByText(`Chat Window Content for role: ${selectedRole}`)).toBeInTheDocument();


    // The original assertion for other text in the page
    expect(screen.getAllByText(selectedRole).length).toBeGreaterThanOrEqual(1); // At least one instance for the role text (e.g. in header)

    expect(mobileView).toBeInTheDocument();
    expect(mobileView).toHaveClass('lg:hidden');

    expect(desktopView).toBeInTheDocument();
    expect(desktopView).toHaveClass('hidden lg:grid');
  })

  it('renders mobile tabbed interface and switches views', () => {
    render(<Page />)
    fireEvent.click(screen.getByText('Select Construction Worker'))
    
    // 1. Check default state (Chat Tab)
    // We expect 2 ChatWindows: 1 in Desktop (always present), 1 in Mobile (active tab)
    expect(screen.getAllByTestId('chat-window')).toHaveLength(2);

    // Verify Tab Bar Buttons exist
    // Using regex to match button text which might be inside spans
    const docsTab = screen.getByRole('button', { name: /Docs/i });
    const articleTab = screen.getByRole('button', { name: /Article/i });
    const chatTab = screen.getByRole('button', { name: /Chat/i });

    expect(docsTab).toBeInTheDocument();
    expect(articleTab).toBeInTheDocument();
    expect(chatTab).toBeInTheDocument();

    const mobileView = screen.getByTestId('mobile-view');

    // 2. Switch to Docs Tab
    fireEvent.click(docsTab);
    
    // Verify Docs Content appears in mobile view
    // Use within to avoid finding desktop elements
    expect(within(mobileView).getByText('Getting Started')).toBeInTheDocument();
    expect(within(mobileView).getByRole('button', { name: 'Introduction' })).toBeInTheDocument();
    
    // Verify ChatWindow in Mobile is gone (total should be 1, from Desktop)
    expect(screen.getAllByTestId('chat-window')).toHaveLength(1);

    // 3. Switch to Article Tab
    fireEvent.click(articleTab);
    
    // Verify Article Content
    expect(within(mobileView).getByText('This is the mobile article view.')).toBeInTheDocument();
    
    // 4. Switch back to Chat Tab
    fireEvent.click(chatTab);
    expect(screen.getAllByTestId('chat-window')).toHaveLength(2);
  })

  it('verifies desktop structure content', () => {
    render(<Page />)
    fireEvent.click(screen.getByText('Select Construction Worker'))
    
    const leftCol = screen.getByTestId('desktop-left-col');
    const middleCol = screen.getByTestId('desktop-middle-col');
    const rightCol = screen.getByTestId('desktop-right-col');

    expect(leftCol).toHaveTextContent('Docs');
    expect(middleCol).toHaveTextContent('Welcome to the HMSREG Documentation'); // Desktop title
    expect(rightCol).toHaveTextContent('AI Assistant');
  })
});