import React from 'react';
import Markdown from 'react-markdown';
import { cn } from "@/lib/utils";
import { SourceCitation } from "@/hooks/use-chat";

export interface ChatBubbleProps {
  role: 'user' | 'assistant';
  content: string;
  citations?: SourceCitation[];
}

export function ChatBubble({ role, content, citations }: ChatBubbleProps) {
  const isUser = role === 'user';

  return (
    <div className={cn(
      "flex w-full mb-4",
      isUser ? "justify-end" : "justify-start"
    )}>
      <div className={cn(
        "max-w-[80%] rounded-lg px-4 py-2 text-sm shadow-sm prose dark:prose-invert prose-sm break-words",
        isUser 
          ? "bg-primary text-primary-foreground rounded-br-none prose-p:text-primary-foreground prose-headings:text-primary-foreground" 
          : "bg-muted text-muted-foreground rounded-bl-none"
      )}>
        <Markdown>{content}</Markdown>

        {citations && citations.length > 0 && (
          <div className="mt-3 pt-2 border-t border-black/10 dark:border-white/10">
            <p className="text-[10px] font-bold uppercase tracking-wider opacity-70 mb-1">Source:</p>
            <ul className="space-y-1">
              {citations.map((citation, idx) => (
                <li key={idx}>
                  <a 
                    href={citation.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-xs text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-1"
                  >
                    {citation.title || citation.url}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
