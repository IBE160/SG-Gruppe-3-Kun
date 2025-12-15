"use client"

import React, { useState, useRef, useEffect, useCallback } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ChatBubble } from "./ChatBubble";
import { Send, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";
import { useChat } from "@/hooks/use-chat";

interface ChatWindowProps {
  className?: string;
  userRole: string | null; // Added userRole prop
}

export function ChatWindow({ className, userRole }: ChatWindowProps) { // Destructure userRole
  const { messages, sendMessage, isLoading } = useChat(userRole); // Pass userRole to useChat
  const [inputValue, setInputValue] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // Use useState with a functional lazy initializer to generate chatSessionId once purely
  const [chatSessionId] = useState<string>(() => Date.now().toString());


  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "nearest",
      inline: "nearest"
    });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSendMessage = useCallback(async (content: string) => {
    if (!content.trim()) return;
    setInputValue(""); // Clear input immediately
    await sendMessage(content);
  }, [setInputValue, sendMessage]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;
    await handleSendMessage(inputValue);
  };

  const handleSuggestionClick = useCallback(async (query: string) => {
    if (isLoading) return;
    await handleSendMessage(query);
  }, [isLoading, handleSendMessage]);

  return (
    <div className={cn("flex flex-col h-full min-h-0 w-full border rounded-xl bg-background shadow-sm overflow-hidden", className)}>
      {/* Chat History */}
      <div className="flex-1 min-h-0 overflow-y-auto p-4 space-y-4" aria-live="polite">
        {messages.length === 0 && (
          <div className="flex h-full items-center justify-center text-muted-foreground text-sm">
            Ask a question about HMSREG documentation...
          </div>
        )}
        
        {messages.map((msg) => (
          <ChatBubble
            key={msg.id}
            role={msg.role}
            content={msg.content}
            citations={msg.citations}
            messageId={msg.id} // Pass messageId
            chatSessionId={chatSessionId} // Pass chatSessionId
            suggestedQueries={msg.suggestedQueries} // Pass suggestedQueries
            onSuggestionClick={handleSuggestionClick} // Pass the handler
            isStreaming={isLoading && msg.id === messages[messages.length - 1]?.id && msg.role === 'assistant'} // Add streaming indicator
          />
        ))}

        {isLoading && messages.length > 0 && messages[messages.length - 1].role === 'user' && (
             <div className="flex w-full justify-start mb-4" role="status" aria-live="polite">
                <div className="bg-muted text-muted-foreground rounded-lg rounded-bl-none px-4 py-2 flex items-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span className="text-xs">Connecting...</span>
                </div>
              </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t p-4 bg-card">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <Input 
            value={inputValue} 
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type your question..."
            disabled={isLoading}
            className="flex-1"
          />
          <Button type="submit" disabled={isLoading || !inputValue.trim()} size="icon">
            <Send className="h-4 w-4" />
            <span className="sr-only">Send</span>
          </Button>
        </form>
      </div>
    </div>
  );
}
