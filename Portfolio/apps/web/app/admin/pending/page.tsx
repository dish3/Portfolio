"use client";

import React, { useState } from "react";
import { AdminHeader } from "@/components/admin/admin-header";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { EmptyState } from "@/components/ui/empty-state";
import { CheckCircle2, XCircle, Sparkles, Clock, GitCommit } from "lucide-react";

interface PendingItem {
  id: string;
  agent: string;
  entity_type: string;
  diff: {
    title: string;
    short_description: string;
    tech_stack: string[];
    github_repo_url: string;
  };
  ai_rationale: string;
  created_at: string;
}

export default function PendingApprovalsPage() {
  const [items, setItems] = useState<PendingItem[]>([]);
  const [reviewedId, setReviewedId] = useState<string | null>(null);

  const handleApprove = (id: string) => {
    setReviewedId(id);
    setTimeout(() => {
      setItems((prev) => prev.filter((i) => i.id !== id));
      setReviewedId(null);
    }, 600);
  };

  const handleReject = (id: string) => {
    setReviewedId(id);
    setTimeout(() => {
      setItems((prev) => prev.filter((i) => i.id !== id));
      setReviewedId(null);
    }, 600);
  };

  return (
    <div className="space-y-6">
      <AdminHeader
        title="Approval Queue"
        description="Review, edit, or reject change proposals submitted by autonomous agents before they mutate live tables."
      />

      {items.length === 0 ? (
        <EmptyState
          title="No pending changes"
          description="All proposed changes have been reviewed. When an autonomous agent ingests new commits or releases, approval cards will appear here."
          icon={<Clock className="w-8 h-8 opacity-80" />}
        />
      ) : (
        <div className="space-y-4">
          {items.map((item) => (
            <Card
              key={item.id}
              accent="amber"
              className={reviewedId === item.id ? "opacity-50 pointer-events-none transition-opacity" : ""}
            >
              <CardHeader className="p-0 space-y-3">
                {/* Agent & Timestamp Header */}
                <div className="flex flex-wrap items-center justify-between text-xs font-mono gap-2">
                  <div className="flex items-center gap-2">
                    <Badge variant="amber">
                      <Sparkles className="w-3 h-3" />
                      <span>{item.agent.replace("_", " ").toUpperCase()}</span>
                    </Badge>
                    <span className="text-foreground-muted">proposes new {item.entity_type}</span>
                  </div>
                  <span className="text-foreground-muted">{item.created_at}</span>
                </div>

                {/* Proposed Title & Description */}
                <div>
                  <h4 className="text-lg font-bold font-mono text-foreground">
                    {item.diff.title}
                  </h4>
                  <p className="text-sm text-foreground-secondary mt-1">
                    {item.diff.short_description}
                  </p>
                </div>

                {/* AI Rationale (Mandatory per specification) */}
                <div className="p-3 rounded-lg bg-surface-subtle border border-border-subtle text-xs text-foreground-secondary">
                  <span className="font-semibold text-accent-amber font-mono">AI Rationale: </span>
                  <span>{item.ai_rationale}</span>
                </div>

                {/* Tech Stack */}
                <div className="flex flex-wrap gap-1.5 pt-1">
                  {item.diff.tech_stack.map((t) => (
                    <Badge key={t} variant="ice" className="text-[11px]">
                      {t}
                    </Badge>
                  ))}
                </div>

                {/* Action Buttons */}
                <div className="pt-4 border-t border-border flex items-center justify-end gap-3">
                  <Button
                    variant="ghost"
                    size="sm"
                    className="gap-1.5 text-red-400 hover:text-red-300"
                    onClick={() => handleReject(item.id)}
                  >
                    <XCircle className="w-4 h-4" />
                    <span>Reject</span>
                  </Button>

                  <Button
                    variant="primary"
                    size="sm"
                    className="gap-1.5"
                    onClick={() => handleApprove(item.id)}
                  >
                    <CheckCircle2 className="w-4 h-4" />
                    <span>Approve & Publish</span>
                  </Button>
                </div>
              </CardHeader>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
