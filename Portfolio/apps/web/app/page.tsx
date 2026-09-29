import Link from "next/link";
import { Sparkles, Terminal, Shield, ArrowRight, Activity } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

export default function HomePage() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-6 relative overflow-hidden">
      {/* Subtle ambient background glow */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-accent-amber/5 blur-[120px] rounded-full pointer-events-none" />

      <div className="max-w-3xl w-full text-center space-y-8 relative z-10">
        {/* Phase Pill */}
        <div className="inline-flex items-center gap-2">
          <Badge variant="amber" className="py-1 px-3">
            <Sparkles className="w-3.5 h-3.5" />
            <span>PROJECT NOVA · PHASE 00 FOUNDATION</span>
          </Badge>
        </div>

        {/* Hero Title */}
        <div className="space-y-4">
          <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-foreground font-mono">
            AI Portfolio OS
          </h1>
          <p className="text-lg sm:text-xl text-foreground-secondary max-w-xl mx-auto font-sans leading-relaxed">
            The portfolio system is currently under construction. Core monorepo
            services, database schema, and authentication architecture are established.
          </p>
        </div>

        {/* Phase 00 Status Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-left pt-4">
          <Card accent="amber">
            <CardHeader className="mb-0">
              <div className="flex items-center gap-2 text-accent-amber mb-2">
                <Terminal className="w-4 h-4" />
                <span className="text-xs font-mono uppercase">Frontend</span>
              </div>
              <CardTitle className="text-base">Next.js 14 Active</CardTitle>
              <CardDescription>
                App Router, Tailwind CSS, Quiet Intelligence design system scaffold.
              </CardDescription>
            </CardHeader>
          </Card>

          <Card accent="ice">
            <CardHeader className="mb-0">
              <div className="flex items-center gap-2 text-accent-ice mb-2">
                <Activity className="w-4 h-4" />
                <span className="text-xs font-mono uppercase">Backend</span>
              </div>
              <CardTitle className="text-base">FastAPI Scaffold</CardTitle>
              <CardDescription>
                Pydantic v2 settings, OpenAPI docs, and /health endpoint verified.
              </CardDescription>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader className="mb-0">
              <div className="flex items-center gap-2 text-foreground-muted mb-2">
                <Shield className="w-4 h-4" />
                <span className="text-xs font-mono uppercase">Governance</span>
              </div>
              <CardTitle className="text-base">Approval Queue</CardTitle>
              <CardDescription>
                AI changes isolated to pending_changes table; human-in-the-loop enforced.
              </CardDescription>
            </CardHeader>
          </Card>
        </div>

        {/* Action Links */}
        <div className="pt-6 flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link
            href="/projects"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-lg bg-accent-amber hover:bg-accent-amber/90 text-[#0A0A0F] font-semibold font-mono text-sm transition-all shadow-md"
          >
            <span>Explore Projects Archive</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
          <Link
            href="/admin"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-lg bg-surface hover:bg-surface-hover border border-border text-foreground font-mono text-sm transition-all shadow-sm hover:border-accent-amber/40"
          >
            <span>Enter Admin Dashboard</span>
            <ArrowRight className="w-4 h-4 text-accent-amber" />
          </Link>
        </div>

        {/* Footer info */}
        <div className="pt-12 text-xs font-mono text-foreground-muted">
          Quiet Intelligence Aesthetic · Autonomous Agent Ingestion · Standalone Monorepo
        </div>
      </div>
    </main>
  );
}
