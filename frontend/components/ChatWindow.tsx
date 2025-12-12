"use client"

import React, { useState, useRef, useEffect } from 'react';
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

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const content = inputValue;
    setInputValue(""); // Clear input immediately
    await sendMessage(content);
  };

  return (
    <div className={cn("flex flex-col h-[600px] w-full max-w-2xl border rounded-xl bg-background shadow-sm overflow-hidden mx-auto", className)}>
      {/* Chat History */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="flex h-full items-center justify-center text-muted-foreground text-sm">
            Ask a question about HMSREG documentation...
          </div>
        )}
        
        {messages.map((msg) => (
          <ChatBubble key={msg.id} role={msg.role} content={msg.content} citations={msg.citations} />
        ))}
        
        {isLoading && messages.length > 0 && messages[messages.length - 1].role === 'user' && (
             <div className="flex w-full justify-start mb-4">
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
