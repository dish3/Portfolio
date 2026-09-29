import * as React from "react";
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "ghost" | "danger";
  size?: "sm" | "md" | "lg";
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "md", ...props }, ref) => {
    const baseStyles =
      "inline-flex items-center justify-center font-medium rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-accent-amber/50 disabled:opacity-50 disabled:pointer-events-none";

    const variants = {
      primary: "bg-accent-amber text-[#0A0A0F] font-semibold hover:bg-accent-amber/90",
      secondary: "bg-surface hover:bg-surface-hover text-foreground border border-border",
      outline: "border border-border text-foreground hover:bg-surface-subtle",
      ghost: "text-foreground-secondary hover:text-foreground hover:bg-surface-subtle",
      danger: "bg-red-900/40 text-red-300 border border-red-800 hover:bg-red-900/60",
    };

    const sizes = {
      sm: "h-8 px-3 text-xs",
      md: "h-10 px-4 text-sm",
      lg: "h-12 px-6 text-base",
    };

    return (
      <button
        ref={ref}
        className={twMerge(clsx(baseStyles, variants[variant], sizes[size], className))}
        {...props}
      />
    );
  }
);
Button.displayName = "Button";
