import React from "react";
import { AdminHeader } from "@/components/admin/admin-header";
import { EmptyState } from "@/components/ui/empty-state";
import { FileText } from "lucide-react";

export default function AdminResumePage() {
  return (
    <div className="space-y-6">
      <AdminHeader
        title="Resume Versions"
        description="Role-targeted resumes (SWE, AI, ML, Backend, ATS) managed dynamically by the Resume Agent."
      />

      <EmptyState
        title="No generated resume versions"
        description="Resume versions will be synthesized by the Resume Agent upon approval of projects and skills in Phase 05."
        icon={<FileText className="w-8 h-8 opacity-80" />}
      />
    </div>
  );
}
