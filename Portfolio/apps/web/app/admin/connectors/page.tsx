import React from "react";
import { AdminHeader } from "@/components/admin/admin-header";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Radio } from "lucide-react";

const REGISTERED_CONNECTORS = [
  { platform: "GitHub", status: "Phase 1", auto: true, desc: "Webhook & poll ingestion for repos, READMEs, commits" },
  { platform: "LeetCode", status: "Phase 6", auto: true, desc: "Public GraphQL statistics poller" },
  { platform: "LinkedIn", status: "Phase 2", auto: false, desc: "Manual URL & caption text submission" },
  { platform: "Kaggle", status: "Future", auto: false, desc: "Competitions and notebooks showcase" },
  { platform: "Devpost", status: "Future", auto: false, desc: "Hackathon project submissions" },
  { platform: "Hashnode", status: "Future", auto: false, desc: "Technical blog post updates" },
  { platform: "Medium", status: "Future", auto: false, desc: "Articles and publications" },
  { platform: "Codeforces", status: "Future", auto: false, desc: "Contest ratings and problem stats" },
  { platform: "HackerRank", status: "Future", auto: false, desc: "Skill certificates and badges" },
  { platform: "Spotify", status: "Future", auto: false, desc: "Currently playing & public playlists" },
  { platform: "Instagram", status: "Future", auto: false, desc: "Photography & creative portfolio feed" },
];

export default function AdminConnectorsPage() {
  return (
    <div className="space-y-6">
      <AdminHeader
        title="Platform Connectors"
        description="External source ingestion interfaces. NOTE: X / Twitter is permanently excluded from this system."
      />

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {REGISTERED_CONNECTORS.map((c) => (
          <Card key={c.platform}>
            <CardHeader className="p-0">
              <div className="flex items-center justify-between mb-2">
                <CardTitle className="text-base font-mono">{c.platform}</CardTitle>
                <Badge variant={c.status === "Phase 1" ? "amber" : "muted"}>
                  {c.status}
                </Badge>
              </div>
              <CardDescription className="text-xs">{c.desc}</CardDescription>
              <div className="pt-4 flex items-center justify-between text-xs font-mono text-foreground-muted">
                <span>{c.auto ? "Automated Sync" : "Manual Link"}</span>
                <span className="text-amber-500/80">Disabled (Phase 00)</span>
              </div>
            </CardHeader>
          </Card>
        ))}
      </div>
    </div>
  );
}
