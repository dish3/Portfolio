import React from "react";
import { AdminHeader } from "@/components/admin/admin-header";
import { EmptyState } from "@/components/ui/empty-state";
import { Milestone } from "lucide-react";

export default function AdminTimelinePage() {
  return (
    <div className="space-y-6">
      <AdminHeader
        title="Experience & Timeline"
        description="Unified chronological feed of hackathons, internships, project launches, and achievements."
      />

      <EmptyState
        title="No timeline events"
        description="The timeline will automatically populate as projects and milestones are approved into the system."
        icon={<Milestone className="w-8 h-8 opacity-80" />}
      />
    </div>
  );
}
