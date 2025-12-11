import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-background">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
        <h1 className="text-4xl font-bold text-primary mb-8">HMSREG Chatbot</h1>
      </div>

      <div className="flex flex-col items-center gap-4">
        <p className="text-lg text-foreground">
          Welcome to the documentation assistant.
        </p>
        
        <div className="flex gap-4">
          <Button>Primary Action</Button>
          <Button variant="secondary">Secondary Action</Button>
          <Button variant="outline">Outline Action</Button>
        </div>
        
        <div className="mt-8 p-4 bg-muted rounded-lg">
          <p className="text-muted-foreground">Tailwind v4 + Shadcn/ui configured successfully.</p>
        </div>
      </div>
    </main>
  );
}