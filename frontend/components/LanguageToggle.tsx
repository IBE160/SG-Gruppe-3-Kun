"use client";

import { useLocale } from 'next-intl';
import { useRouter, usePathname } from '@/lib/i18n/navigation';
import { Button } from '@/components/ui/button';
import { locales, type Locale } from '@/lib/i18n/config';
import { useEffect, useState } from 'react';

function setLanguagePreference(newLocale: string) {
  if (typeof window !== 'undefined') {
    localStorage.setItem('preferred-locale', newLocale);
    document.cookie = `preferred-locale=${newLocale}; path=/; max-age=31536000`;
  }
}

export function LanguageToggle() {
  const locale = useLocale() as Locale;
  const router = useRouter();
  const pathname = usePathname();
  const [mounted, setMounted] = useState(false);

  useEffect(() => setMounted(true), []);

  const switchLocale = (newLocale: Locale) => {
    setLanguagePreference(newLocale);
    router.replace(pathname, { locale: newLocale });
  };

  if (!mounted) {
    return (
      <Button variant="ghost" size="sm" disabled>
        <span className="text-sm">...</span>
      </Button>
    );
  }

  return (
    <div className="flex gap-1">
      {locales.map((loc) => (
        <Button
          key={loc}
          variant={locale === loc ? "default" : "ghost"}
          size="sm"
          onClick={() => switchLocale(loc)}
          className="text-xs"
        >
          {loc.toUpperCase()}
        </Button>
      ))}
    </div>
  );
}
