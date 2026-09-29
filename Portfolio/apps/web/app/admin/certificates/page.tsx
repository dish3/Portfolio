import React from "react";
import { AdminHeader } from "@/components/admin/admin-header";
import { EmptyState } from "@/components/ui/empty-state";
import { Award } from "lucide-react";

export default function AdminCertificatesPage() {
  return (
    <div className="space-y-6">
      <AdminHeader
        title="Certificates & Credentials"
        description="Verified certificates extracted from external platforms and manual submissions."
      />

      <EmptyState
        title="No certificates"
        description="No certificates have been ingested yet. You can submit credential links or LinkedIn posts for Content Agent processing."
        icon={<Award className="w-8 h-8 opacity-80" />}
      />
    </div>
  );
}
