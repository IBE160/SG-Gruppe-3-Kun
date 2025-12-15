"use client"

import * as React from "react"
import { useTranslations } from 'next-intl'
import { Button } from "@/components/ui/button"

export interface RoleSelectorProps {
  onSelect: (role: string) => void;
}

export function RoleSelector({ onSelect }: RoleSelectorProps) {
  const t = useTranslations('roleSelector');

  // Map keys to backend enum values (always English)
  const backendRoleMap: Record<string, string> = {
    'constructionWorker': 'Construction Worker',
    'supplier': 'Supplier / Subcontractor',
    'projectManager': 'Project Manager / Admin',
  };

  const roles = [
    { key: 'constructionWorker', label: t('roles.constructionWorker'), backendValue: backendRoleMap.constructionWorker },
    { key: 'supplier', label: t('roles.supplier'), backendValue: backendRoleMap.supplier },
    { key: 'projectManager', label: t('roles.projectManager'), backendValue: backendRoleMap.projectManager },
  ];

  return (
    <div className="flex flex-col gap-4 p-6 border rounded-lg shadow-sm bg-card text-card-foreground max-w-sm w-full mx-auto">
      <h2 className="text-xl font-semibold text-center">{t('heading')}</h2>
      <div className="flex flex-col gap-3">
        {roles.map((role) => (
          <Button
            key={role.key}
            variant="outline"
            onClick={() => onSelect(role.backendValue)}
            className="w-full justify-center h-12 text-base"
          >
            {role.label}
          </Button>
        ))}
      </div>
    </div>
  )
}
