import * as React from "react";
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  accent?: "none" | "amber" | "ice";
}

export function Card({
  className,
  accent = "none",
  children,
  ...props
}: CardProps) {
  const accentBorder = {
    none: "border-border",
    amber: "border-accent-amber/40 shadow-[0_0_15px_rgba(217,168,87,0.05)]",
    ice: "border-accent-ice/40 shadow-[0_0_15px_rgba(127,231,224,0.05)]",
  };

  return (
    <div
      className={twMerge(
        clsx(
          "bg-surface/80 backdrop-blur-md rounded-xl border p-6 text-foreground",
          accentBorder[accent],
          className
        )
      )}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardHeader({
  className,
  children,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={twMerge(clsx("mb-4 flex flex-col space-y-1.5", className))} {...props}>
      {children}
    </div>
  );
}

export function CardTitle({
  className,
  children,
  ...props
}: React.HTMLAttributes<HTMLHeadingElement>) {
  return (
    <h3
      className={twMerge(
        clsx("text-lg font-semibold tracking-tight text-foreground", className)
      )}
      {...props}
    >
      {children}
    </h3>
  );
}

export function CardDescription({
  className,
  children,
  ...props
}: React.HTMLAttributes<HTMLParagraphElement>) {
  return (
    <p
      className={twMerge(clsx("text-sm text-foreground-secondary", className))}
      {...props}
    >
      {children}
    </p>
  );
}
