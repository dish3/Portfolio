import React from "react";
import Link from "next/link";
import { Lock, ArrowLeft, Shield } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function AdminLoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center p-6 bg-background">
      <div className="max-w-md w-full">
        <Card accent="amber">
          <CardHeader className="text-center space-y-2">
            <div className="w-12 h-12 rounded-xl bg-accent-amber/10 border border-accent-amber/30 text-accent-amber mx-auto flex items-center justify-center mb-2">
              <Lock className="w-6 h-6" />
            </div>
            <CardTitle className="text-xl font-mono">NOVA OS Authentication</CardTitle>
            <CardDescription className="text-xs">
              Administrative credentials required. Authentication skeleton is established for Supabase / NextAuth integration.
            </CardDescription>
          </CardHeader>

          <div className="space-y-4 pt-4 border-t border-border">
            <div className="p-3 rounded-lg bg-surface-subtle border border-border-subtle text-xs text-foreground-secondary space-y-1">
              <div className="flex items-center gap-1.5 text-accent-amber font-semibold font-mono">
                <Shield className="w-3.5 h-3.5" />
                <span>Phase 00 Skeleton Mode</span>
              </div>
              <p>
                In development, navigate directly to <code className="text-foreground font-mono">/admin</code> with dev bypass or set the session cookie.
              </p>
            </div>

            <Link href="/admin" className="block">
              <Button variant="primary" className="w-full">
                Enter Admin Dashboard Shell
              </Button>
            </Link>

            <Link href="/" className="inline-flex items-center gap-1.5 text-xs font-mono text-foreground-muted hover:text-foreground">
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>Return to Public Site</span>
            </Link>
          </div>
        </Card>
      </div>
    </div>
  );
}
