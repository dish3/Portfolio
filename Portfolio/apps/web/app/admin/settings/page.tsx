import React from "react";
import { AdminHeader } from "@/components/admin/admin-header";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function AdminSettingsPage() {
  return (
    <div className="space-y-6">
      <AdminHeader
        title="System Settings"
        description="System configuration, environment variables, and authentication parameters."
      />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card>
          <CardHeader className="p-0 space-y-2">
            <CardTitle className="text-base font-mono">Environment Configuration</CardTitle>
            <CardDescription className="text-xs">
              System is running in development mode. Secrets are managed via backend environment variables.
            </CardDescription>
            <div className="pt-2">
              <Badge variant="amber">Phase 00 Foundation</Badge>
            </div>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader className="p-0 space-y-2">
            <CardTitle className="text-base font-mono">Authentication Architecture</CardTitle>
            <CardDescription className="text-xs">
              Protected admin middleware is active. Pluggable authentication skeleton with NextAuth / Supabase.
            </CardDescription>
            <div className="pt-2">
              <Badge variant="success">Middleware Active</Badge>
            </div>
          </CardHeader>
        </Card>
      </div>
    </div>
  );
}
