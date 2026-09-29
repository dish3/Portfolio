import { ShieldCheck, Cpu } from "lucide-react";
import { Badge } from "@/components/ui/badge";

interface AdminHeaderProps {
  title: string;
  description?: string;
}

export function AdminHeader({ title, description }: AdminHeaderProps) {
  return (
    <header className="flex flex-col md:flex-row md:items-center justify-between pb-6 mb-6 border-b border-border gap-4">
      <div>
        <h2 className="text-2xl font-bold tracking-tight text-foreground font-mono">
          {title}
        </h2>
        {description && (
          <p className="text-sm text-foreground-secondary mt-1">{description}</p>
        )}
      </div>

      <div className="flex items-center gap-3">
        <Badge variant="amber" className="py-1">
          <Cpu className="w-3.5 h-3.5" />
          <span>AI Engine: Standby</span>
        </Badge>
        <Badge variant="success" className="py-1">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>Protected Route</span>
        </Badge>
      </div>
    </header>
  );
}
