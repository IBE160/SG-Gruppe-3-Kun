import { useState, useCallback } from 'react';

export interface SourceCitation {
  title: string;
  url: string;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  citations?: SourceCitation[];
}

export function useChat(userRole: string | null) { // Added userRole parameter
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    // Placeholder for assistant message
    const assistantId = (Date.now() + 1).toString();
    setMessages((prev) => [...prev, { id: assistantId, role: 'assistant', content: '' }]);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: content, user_role: userRole }), // Changed 'role' to 'user_role' and used userRole
      });

      if (!response.ok) throw new Error('Network response was not ok');
      if (!response.body) throw new Error('No body');

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        buffer += chunk;
        
        const lines = buffer.split('\n\n');
        // Keep the last partial line in buffer
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const dataStr = line.slice(6);
            if (dataStr === '[DONE]') continue;
            
            try {
              const data = JSON.parse(dataStr);
              if (data.type === 'token') {
                setMessages((prev) => 
                  prev.map((msg) => 
                    msg.id === assistantId 
                      ? { ...msg, content: msg.content + data.content } 
                      : msg
                  )
                );
              } else if (data.type === 'citation') {
                setMessages((prev) => 
                  prev.map((msg) => 
                    msg.id === assistantId 
                      ? { ...msg, citations: data.content } 
                      : msg
                  )
                );
              } else if (data.type === 'error') {
                 console.error("Backend error:", data.content);
                 setMessages((prev) => 
                    prev.map((msg) => 
                      msg.id === assistantId 
                        ? { ...msg, content: msg.content + "\n\n[Error: " + data.content + "]" } 
                        : msg
                    )
                  );
              }
            } catch (e) {
              console.error('Error parsing SSE:', e);
            }
          }
        }
      }
      setIsLoading(false); // Set to false when stream is complete

    } catch (error) {
      console.error('Chat error:', error);
      setMessages((prev) => 
        prev.map((msg) => 
          msg.id === assistantId 
            ? { ...msg, content: msg.content + "\n\n[System Error: Failed to connect to chat service.]" } 
            : msg
        )
      );
      setIsLoading(false); // Also set to false on error
    }
  }, [userRole]);

  return { messages, sendMessage, isLoading };
}
