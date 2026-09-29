import * as React from "react";
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "default" | "amber" | "ice" | "success" | "warning" | "danger" | "muted";
}

export function Badge({
  className,
  variant = "default",
  children,
  ...props
}: BadgeProps) {
  const variants = {
    default: "bg-surface-hover text-foreground border-border",
    amber: "bg-accent-amber/10 text-accent-amber border-accent-amber/30",
    ice: "bg-accent-ice/10 text-accent-ice border-accent-ice/30",
    success: "bg-emerald-950/40 text-emerald-400 border-emerald-800/50",
    warning: "bg-amber-950/40 text-amber-400 border-amber-800/50",
    danger: "bg-red-950/40 text-red-400 border-red-800/50",
    muted: "bg-surface-subtle text-foreground-muted border-border-subtle",
  };

  return (
    <span
      className={twMerge(
        clsx(
          "inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-mono border",
          variants[variant],
          className
        )
      )}
      {...props}
    >
      {children}
    </span>
  );
}
