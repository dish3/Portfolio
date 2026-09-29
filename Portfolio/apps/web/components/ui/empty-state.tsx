import React from "react";
import { Inbox } from "lucide-react";

interface EmptyStateProps {
  title?: string;
  description?: string;
  icon?: React.ReactNode;
}

export function EmptyState({
  title = "No pending changes",
  description = "The approval queue is clear. Autonomous agents will submit proposals here upon noticing external changes.",
  icon,
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center p-12 text-center rounded-xl border border-dashed border-border bg-surface/40 my-6">
      <div className="p-4 rounded-full bg-surface-hover/80 text-accent-amber mb-4 border border-border">
        {icon || <Inbox className="w-8 h-8 opacity-80" />}
      </div>
      <h3 className="text-lg font-semibold text-foreground mb-1">{title}</h3>
      <p className="text-sm text-foreground-secondary max-w-md">{description}</p>
    </div>
  );
}
