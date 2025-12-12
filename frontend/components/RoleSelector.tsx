import * as React from "react"
import { Button } from "@/components/ui/button"

export interface RoleSelectorProps {
  onSelect: (role: string) => void;
}

const roles = [
  "Construction Worker",
  "Supplier",
  "Project Manager"
];

export function RoleSelector({ onSelect }: RoleSelectorProps) {
  return (
    <div className="flex flex-col gap-4 p-6 border rounded-lg shadow-sm bg-card text-card-foreground max-w-sm w-full mx-auto">
      <h2 className="text-xl font-semibold text-center">Select Your Role</h2>
      <div className="flex flex-col gap-3">
        {roles.map((role) => (
          <Button 
            key={role} 
            variant="outline" 
            onClick={() => onSelect(role)}
            className="w-full justify-center h-12 text-base"
          >
            {role}
          </Button>
        ))}
      </div>
    </div>
  )
}
