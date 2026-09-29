"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Clock,
  FolderGit2,
  Award,
  Milestone,
  FileText,
  Radio,
  BarChart3,
  Settings,
  Sparkles,
  ExternalLink,
} from "lucide-react";
import { clsx } from "clsx";

export const NAV_ITEMS = [
  { name: "Dashboard", href: "/admin", icon: LayoutDashboard },
  { name: "Pending Approvals", href: "/admin/pending", icon: Clock },
  { name: "Projects", href: "/admin/projects", icon: FolderGit2 },
  { name: "Certificates", href: "/admin/certificates", icon: Award },
  { name: "Timeline", href: "/admin/timeline", icon: Milestone },
  { name: "Resume Versions", href: "/admin/resume", icon: FileText },
  { name: "Connectors", href: "/admin/connectors", icon: Radio },
  { name: "Analytics", href: "/admin/analytics", icon: BarChart3 },
  { name: "Settings", href: "/admin/settings", icon: Settings },
];

export function AdminSidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 border-r border-border bg-surface/90 backdrop-blur-md flex flex-col h-screen sticky top-0">
      {/* Brand Header */}
      <div className="p-6 border-b border-border flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-accent-amber/15 border border-accent-amber/30 flex items-center justify-center text-accent-amber">
            <Sparkles className="w-4 h-4" />
          </div>
          <div>
            <h1 className="font-semibold text-foreground text-sm tracking-wider uppercase font-mono">
              NOVA OS
            </h1>
            <p className="text-xs text-foreground-muted font-mono">v0.1.0 · Admin</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-1.5 overflow-y-auto">
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={clsx(
                "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors font-medium",
                isActive
                  ? "bg-accent-amber/10 text-accent-amber border border-accent-amber/20"
                  : "text-foreground-secondary hover:text-foreground hover:bg-surface-hover"
              )}
            >
              <Icon className={clsx("w-4 h-4", isActive ? "text-accent-amber" : "text-foreground-muted")} />
              <span>{item.name}</span>
            </Link>
          );
        })}
      </nav>

      {/* Footer link to public site */}
      <div className="p-4 border-t border-border">
        <Link
          href="/"
          className="flex items-center justify-between px-3 py-2 rounded-lg text-xs font-mono text-foreground-secondary hover:text-foreground hover:bg-surface-hover transition-colors"
        >
          <span>View Public Site</span>
          <ExternalLink className="w-3.5 h-3.5" />
        </Link>
      </div>
    </aside>
  );
}
