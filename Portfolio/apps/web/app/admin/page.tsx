import React from "react";
import { AdminHeader } from "@/components/admin/admin-header";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/empty-state";
import { Clock, FolderGit2, Radio, Sparkles } from "lucide-react";

export default function AdminDashboardPage() {
  return (
    <div className="space-y-6">
      <AdminHeader
        title="Admin Control Surface"
        description="Autonomous agent queue, live portfolio status, and connector ingestion controls."
      />

      {/* Metrics Row (Zero state — no fake data) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="p-0">
            <div className="flex items-center justify-between text-foreground-muted mb-2">
              <span className="text-xs font-mono uppercase">Pending Approvals</span>
              <Clock className="w-4 h-4 text-accent-amber" />
            </div>
            <div className="text-3xl font-bold font-mono text-foreground">0</div>
            <CardDescription className="text-xs mt-1">Awaiting human review</CardDescription>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader className="p-0">
            <div className="flex items-center justify-between text-foreground-muted mb-2">
              <span className="text-xs font-mono uppercase">Published Projects</span>
              <FolderGit2 className="w-4 h-4 text-accent-ice" />
            </div>
            <div className="text-3xl font-bold font-mono text-foreground">0</div>
            <CardDescription className="text-xs mt-1">Live in knowledge graph</CardDescription>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader className="p-0">
            <div className="flex items-center justify-between text-foreground-muted mb-2">
              <span className="text-xs font-mono uppercase">Active Connectors</span>
              <Radio className="w-4 h-4 text-foreground-secondary" />
            </div>
            <div className="text-3xl font-bold font-mono text-foreground">0</div>
            <CardDescription className="text-xs mt-1">Ingestion pipelines enabled</CardDescription>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader className="p-0">
            <div className="flex items-center justify-between text-foreground-muted mb-2">
              <span className="text-xs font-mono uppercase">Active Agents</span>
              <Sparkles className="w-4 h-4 text-accent-amber" />
            </div>
            <div className="text-3xl font-bold font-mono text-foreground">7</div>
            <CardDescription className="text-xs mt-1">Standby for triggers</CardDescription>
          </CardHeader>
        </Card>
      </div>

      {/* Primary Section: Approval Queue */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-base font-semibold text-foreground font-mono">
            Approval Queue
          </h3>
          <span className="text-xs font-mono text-foreground-muted">
            pending_changes table
          </span>
        </div>

        {/* Empty state per specification: "No pending changes" */}
        <EmptyState
          title="No pending changes"
          description="Autonomous agents have not proposed any updates yet. Incoming GitHub commits and external submissions will generate review cards here."
        />
      </div>
    </div>
  );
}
