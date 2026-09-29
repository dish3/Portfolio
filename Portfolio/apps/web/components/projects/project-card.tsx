import React from "react";
import Link from "next/link";
import { ExternalLink, GitBranch, ArrowUpRight } from "lucide-react";
import { Project } from "@nova/types";
import { Badge } from "@/components/ui/badge";

interface ProjectCardProps {
  project: Project;
}

export function ProjectCard({ project }: ProjectCardProps) {
  return (
    <div className="group relative rounded-xl border border-border bg-surface/80 p-6 backdrop-blur-md transition-all hover:border-accent-amber/40 hover:shadow-[0_0_25px_rgba(217,168,87,0.06)] flex flex-col justify-between">
      <div className="space-y-4">
        {/* Top Badges & Meta */}
        <div className="flex items-center justify-between text-xs font-mono text-foreground-muted">
          <div className="flex items-center gap-1.5">
            <GitBranch className="w-3.5 h-3.5 text-accent-amber" />
            <span className="capitalize">{project.source}</span>
          </div>
          {project.started_at && <span>{project.started_at}</span>}
        </div>

        {/* Project Title & Link */}
        <div>
          <Link
            href={`/projects/${project.slug}`}
            className="inline-flex items-center gap-1.5 text-xl font-bold font-mono text-foreground group-hover:text-accent-amber transition-colors"
          >
            <span>{project.title}</span>
            <ArrowUpRight className="w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity" />
          </Link>
          <p className="mt-2 text-sm text-foreground-secondary line-clamp-3 leading-relaxed">
            {project.short_description || "Autonomous AI portfolio system component."}
          </p>
        </div>

        {/* Tech Stack Badges */}
        <div className="flex flex-wrap gap-1.5 pt-2">
          {project.tech_stack.slice(0, 5).map((tech) => (
            <Badge key={tech} variant="default" className="text-[11px] py-0">
              {tech}
            </Badge>
          ))}
          {project.tech_stack.length > 5 && (
            <span className="text-[11px] font-mono text-foreground-muted self-center">
              +{project.tech_stack.length - 5}
            </span>
          )}
        </div>
      </div>

      {/* Action Links */}
      <div className="mt-6 pt-4 border-t border-border/80 flex items-center justify-between text-xs font-mono">
        <Link
          href={`/projects/${project.slug}`}
          className="text-accent-amber hover:underline inline-flex items-center gap-1"
        >
          <span>View Details</span>
          <ArrowUpRight className="w-3.5 h-3.5" />
        </Link>

        <div className="flex items-center gap-3 text-foreground-secondary">
          {project.github_repo_url && (
            <a
              href={project.github_repo_url}
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-foreground transition-colors"
              title="GitHub Repository"
            >
              <ExternalLink className="w-4 h-4" />
            </a>
          )}
        </div>
      </div>
    </div>
  );
}
