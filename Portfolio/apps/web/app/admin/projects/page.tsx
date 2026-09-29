import React from "react";
import { AdminHeader } from "@/components/admin/admin-header";
import { EmptyState } from "@/components/ui/empty-state";
import { FolderGit2 } from "lucide-react";

export default function AdminProjectsPage() {
  return (
    <div className="space-y-6">
      <AdminHeader
        title="Live Projects"
        description="Projects published to the knowledge graph. Modified only via approved pending changes."
      />

      <EmptyState
        title="No published projects"
        description="No projects have been approved to the live portfolio yet. GitHub Agent proposals will appear under Pending Approvals."
        icon={<FolderGit2 className="w-8 h-8 opacity-80" />}
      />
    </div>
  );
}
