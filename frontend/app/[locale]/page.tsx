"use client"

import { useState } from "react";
import { useTranslations } from 'next-intl';
import { Button } from "@/components/ui/button";
import { RoleSelector } from "@/components/RoleSelector";
import { ChatWindow } from "@/components/ChatWindow";
import { LanguageToggle } from "@/components/LanguageToggle";
import { ThemeToggle } from "@/components/ThemeToggle";
import { Book, FileText, Settings, User, MessageSquare } from "lucide-react";

export default function Home() {
  const t = useTranslations();
  const [userRole, setUserRole] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'links' | 'article' | 'chat'>('chat');

  // Get translated role label
  const getRoleLabel = (roleKey: string) => {
    return t(`roleSelector.roles.${roleKey}`);
  };

  if (!userRole) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center p-8 bg-slate-50">
        <div className="mb-8 text-center">
             <h1 className="text-4xl font-bold text-primary mb-2">{t('roleSelector.title')}</h1>
             <p className="text-slate-600">{t('roleSelector.subtitle')}</p>
        </div>
        <RoleSelector onSelect={setUserRole} />
        <div className="mt-6 flex items-center gap-2">
          <ThemeToggle />
          <LanguageToggle />
        </div>
      </main>
    );
  }

  return (
    <main className="h-screen bg-background overflow-hidden">
      {/* Mobile View (< 1024px) */}
      <div data-testid="mobile-view" className="lg:hidden flex flex-col h-full bg-slate-50">
          <header className="p-4 border-b bg-white flex justify-between items-center shadow-sm z-10">
              <h1 className="font-bold text-lg text-primary">HMSREG</h1>
              <div className="flex items-center gap-2">
                <ThemeToggle />
                <LanguageToggle />
                <Button variant="ghost" size="sm" onClick={() => setUserRole(null)}>
                    <User className="h-4 w-4 mr-2" />
                    <span className="truncate max-w-[100px]">{getRoleLabel(userRole)}</span>
                </Button>
              </div>
          </header>

          <div className="flex-1 min-h-0 overflow-hidden relative">
               {activeTab === 'links' && (
                   <div className="h-full overflow-y-auto p-4">
                       <h2 className="font-bold mb-4 text-lg px-1">{t('documentation.title')}</h2>
                       <nav className="space-y-2">
                            <p className="px-2 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">{t('navigation.gettingStarted')}</p>
                            <button className="w-full text-left p-3 bg-white rounded-lg shadow-sm border hover:border-primary transition-colors text-sm font-medium text-slate-700">{t('documentation.introduction')}</button>
                            <button className="w-full text-left p-3 bg-white rounded-lg shadow-sm border hover:border-primary transition-colors text-sm font-medium text-slate-700">{t('documentation.installation')}</button>

                            <p className="px-2 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2 mt-4">{t('navigation.coreConcepts')}</p>
                            <button className="w-full text-left p-3 bg-white rounded-lg shadow-sm border hover:border-primary transition-colors text-sm font-medium text-slate-700">{t('documentation.architecture')}</button>
                            <button className="w-full text-left p-3 bg-white rounded-lg shadow-sm border hover:border-primary transition-colors text-sm font-medium text-slate-700">{t('documentation.authentication')}</button>
                       </nav>
                   </div>
               )}

               {activeTab === 'article' && (
                   <div className="h-full overflow-y-auto p-4 bg-white">
                        <article className="prose prose-slate max-w-none">
                            <h1>{t('documentation.welcomeMobile')}</h1>
                            <p>{t('documentation.welcomeMobileText')}</p>
                            <div className="my-8 p-6 bg-slate-50 rounded-lg border border-dashed border-slate-300 flex flex-col items-center justify-center text-slate-400 gap-2 h-64">
                                <FileText className="h-8 w-8 opacity-50" />
                                <span>{t('documentation.articleContent')}</span>
                            </div>
                        </article>
                   </div>
               )}

               {activeTab === 'chat' && (
                   <ChatWindow className="h-full border-none shadow-none rounded-none max-w-none" userRole={userRole} />
               )}
          </div>

          {/* Bottom Tab Bar */}
          <div className="border-t bg-white flex justify-around items-center h-16 pb-2 z-10 shadow-[0_-1px_3px_rgba(0,0,0,0.05)]">
              <Button
                variant="ghost"
                className={`flex-1 flex flex-col items-center justify-center gap-1 h-full rounded-none hover:bg-slate-50 ${activeTab === 'links' ? 'text-primary' : 'text-slate-500'}`}
                onClick={() => setActiveTab('links')}
              >
                 <Book className="h-5 w-5" />
                 <span className="text-[10px] font-medium">{t('navigation.docs')}</span>
              </Button>

              <Button
                variant="ghost"
                className={`flex-1 flex flex-col items-center justify-center gap-1 h-full rounded-none hover:bg-slate-50 ${activeTab === 'article' ? 'text-primary' : 'text-slate-500'}`}
                onClick={() => setActiveTab('article')}
              >
                 <FileText className="h-5 w-5" />
                 <span className="text-[10px] font-medium">{t('navigation.article')}</span>
              </Button>

              <Button
                variant="ghost"
                className={`flex-1 flex flex-col items-center justify-center gap-1 h-full rounded-none hover:bg-slate-50 ${activeTab === 'chat' ? 'text-primary' : 'text-slate-500'}`}
                onClick={() => setActiveTab('chat')}
              >
                 <MessageSquare className="h-5 w-5" />
                 <span className="text-[10px] font-medium">{t('navigation.chat')}</span>
              </Button>
          </div>
      </div>

      {/* Desktop View (>= 1024px) */}
      <div data-testid="desktop-view" className="hidden lg:grid lg:grid-cols-12 h-full overflow-hidden">
        
        {/* Left Column: Navigation (20% -> 2-3 cols out of 12) */}
        <div data-testid="desktop-left-col" className="col-span-3 xl:col-span-2 border-r bg-slate-50 flex flex-col">
            <div className="p-4 border-b bg-white">
                <h2 className="font-bold flex items-center gap-2">
                    <Book className="h-5 w-5 text-primary" />
                    {t('navigation.docs')}
                </h2>
            </div>

            <div className="flex-1 overflow-y-auto p-4">
                <nav className="space-y-1">
                    <p className="px-2 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">{t('navigation.gettingStarted')}</p>
                    <button className="block w-full text-left p-3 bg-white rounded-lg shadow-sm border hover:border-primary transition-colors text-sm font-medium text-slate-700">{t('documentation.introduction')}</button>
                    <button className="block w-full text-left p-3 bg-white rounded-lg shadow-sm border hover:border-primary transition-colors text-sm font-medium text-slate-700">{t('documentation.installation')}</button>

                    <p className="px-2 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2 mt-4">{t('navigation.coreConcepts')}</p>
                    <button className="w-full text-left p-3 bg-white rounded-lg shadow-sm border hover:border-primary transition-colors text-sm font-medium text-slate-700">{t('documentation.architecture')}</button>
                    <button className="w-full text-left p-3 bg-white rounded-lg shadow-sm border hover:border-primary transition-colors text-sm font-medium text-slate-700">{t('documentation.authentication')}</button>
                </nav>
            </div>

            <div className="p-4 border-t bg-white">
                <div className="flex items-center justify-between mb-3">
                     <div className="flex items-center gap-2 text-sm text-slate-600">
                         <User className="h-4 w-4" />
                         <span>{getRoleLabel(userRole)}</span>
                     </div>
                     <Button variant="ghost" size="icon" onClick={() => setUserRole(null)} title={t('navigation.changeRole')}>
                         <Settings className="h-4 w-4" />
                     </Button>
                </div>
                <div className="flex items-center gap-2">
                  <ThemeToggle />
                  <LanguageToggle />
                </div>
            </div>
        </div>

        {/* Middle Column: Article Content (50% -> 6-7 cols out of 12) */}
        <div data-testid="desktop-middle-col" className="col-span-5 xl:col-span-7 bg-white overflow-y-auto">
             <div className="max-w-4xl mx-auto p-8 lg:p-12">
                <article className="prose prose-slate max-w-none">
                    <h1>{t('documentation.welcomeTitle')}</h1>
                    <p className="lead">
                        {t('documentation.welcomeLead')}
                    </p>
                    <div className="my-8 p-6 bg-slate-50 rounded-lg border border-dashed border-slate-300 flex flex-col items-center justify-center text-slate-400 gap-2 h-96">
                        <FileText className="h-12 w-12 opacity-50" />
                        <span>{t('documentation.articleLoadsHere')}</span>
                    </div>
                    <h2>{t('documentation.howToUse')}</h2>
                    <p>
                        {t('documentation.howToUseText')}
                    </p>
                </article>
             </div>
        </div>

        {/* Right Column: Chatbot (30% -> 3-4 cols out of 12) */}
        <div data-testid="desktop-right-col" className="col-span-4 xl:col-span-3 border-l bg-white flex flex-col min-h-0">
            <div className="p-4 border-b bg-white flex items-center justify-between">
                <h2 className="font-semibold text-sm uppercase tracking-wider text-slate-500">{t('navigation.aiAssistant')}</h2>
            </div>
            <div className="flex-1 min-h-0 overflow-hidden relative">
                 {/* ChatWindow needs to fill this space */}
                 <ChatWindow className="h-full border-none shadow-none rounded-none max-w-none" userRole={userRole} />
            </div>
        </div>

      </div>
    </main>
  );
}


