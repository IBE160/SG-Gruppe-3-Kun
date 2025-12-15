"use client";

import * as React from "react";
import { useTranslations } from 'next-intl';
import { ThumbsUp, ThumbsDown } from "lucide-react";
import { cn } from "@/lib/utils"; // Assuming a utility for class names
import { Button } from "@/components/ui/button"; // Assuming shadcn/ui button

interface FeedbackButtonsProps {
  messageId: string;
  chatSessionId: string;
}

export function FeedbackButtons({ messageId, chatSessionId }: FeedbackButtonsProps) {
  const t = useTranslations('feedback');
  const [feedbackGiven, setFeedbackGiven] = React.useState<"up" | "down" | null>(null);
  const [isLoading, setIsLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  const handleFeedback = async (rating: "thumbs_up" | "thumbs_down") => {
    if (feedbackGiven || isLoading) {
      return; // Prevent multiple submissions or submissions while loading
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch("/api/v1/feedback/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          chat_session_id: chatSessionId,
          message_id: messageId,
          rating: rating,
          // user_id: "anonymous" // Could be added if user tracking is implemented
        }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error(`Feedback submission failed: ${response.status} ${response.statusText}`, errorText);
        throw new Error(`Error: ${response.status} ${response.statusText} - ${errorText}`);
      }

      setFeedbackGiven(rating === "thumbs_up" ? "up" : "down");
      // Optional: show a toast notification "Thank you for your feedback!"
    } catch (err) {
      console.error("Failed to submit feedback:", err);
      setError(t('error'));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex space-x-2 items-center">
      {feedbackGiven ? (
        <span className="text-sm text-muted-foreground">
          {feedbackGiven === "up" ? t('thanksUp') : t('thanksDown')}
        </span>
      ) : (
        <>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => handleFeedback("thumbs_up")}
            disabled={isLoading}
            className={cn(
              "text-muted-foreground hover:text-green-500",
              isLoading && "cursor-not-allowed opacity-50"
            )}
            aria-label={t('thumbsUp')}
          >
            <ThumbsUp className="h-4 w-4" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => handleFeedback("thumbs_down")}
            disabled={isLoading}
            className={cn(
              "text-muted-foreground hover:text-red-500",
              isLoading && "cursor-not-allowed opacity-50"
            )}
            aria-label={t('thumbsDown')}
          >
            <ThumbsDown className="h-4 w-4" />
          </Button>
          {error && <p className="text-red-500 text-sm">{error}</p>}
        </>
      )}
    </div>
  );
}
