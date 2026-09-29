import React from "react";
import Link from "next/link";
import { ArrowLeft, FolderGit2, Sparkles } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { ProjectCard } from "@/components/projects/project-card";
import { ApiClient } from "@/lib/api-client";
import { Project } from "@nova/types";

// Default fallback projects for development before backend or database is populated
const FALLBACK_PROJECTS: Project[] = [
  {
    id: "e4a2c1b0-9876-4321-b012-3456789abcde",
    slug: "nova-ai-portfolio-os",
    title: "NOVA AI Portfolio OS",
    short_description: "An autonomous AI-managed Operating System and story-driven portfolio built with Next.js 14 and FastAPI.",
    long_description: (
      "NOVA is an intelligent personal operating system designed to ingest developer activity across GitHub, " +
      "synthesize project records using Gemini AI models, and preserve a verified knowledge graph with pgvector. " +
      "All autonomous proposals pass through an approval state machine before mutating live portfolio entities."
    ),
    source: "github",
    github_repo_url: "https://github.com/dish3/ai-portfolio-os",
    live_demo_url: "https://portfolio.os",
    drive_fallback_url: null,
    linkedin_post_url: null,
    youtube_video_url: null,
    cover_image_url: null,
    tech_stack: ["FastAPI", "Next.js", "Python", "TypeScript", "PostgreSQL", "pgvector", "Tailwind CSS"],
    status: "published",
    started_at: "2026-09-01",
    updated_at: "2026-09-29T20:00:00Z",
  }
];

export const revalidate = 3600; // On-demand ISR fallback 1 hour

export default async function ProjectsPage() {
  let projects: Project[] = [];

  try {
    projects = await ApiClient.getProjects();
  } catch (error) {
    // Graceful fallback during static build or backend cold start
    projects = FALLBACK_PROJECTS;
  }

  if (!projects || projects.length === 0) {
    projects = FALLBACK_PROJECTS;
  }

  return (
    <main className="min-h-screen py-16 px-6 max-w-7xl mx-auto">
      {/* Navigation Header */}
      <div className="mb-10 flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-border pb-6">
        <div>
          <Link
            href="/"
            className="inline-flex items-center gap-1.5 text-xs font-mono text-foreground-muted hover:text-accent-amber mb-3 transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Return to Arrival</span>
          </Link>
          <div className="flex items-center gap-2.5">
            <h1 className="text-3xl sm:text-4xl font-extrabold font-mono text-foreground tracking-tight">
              Projects Archive
            </h1>
            <Badge variant="amber" className="hidden sm:inline-flex">
              <Sparkles className="w-3 h-3" />
              <span>Phase 1 Knowledge Graph</span>
            </Badge>
          </div>
          <p className="text-sm text-foreground-secondary mt-1">
            Engineered software systems, research artifacts, and production platforms.
          </p>
        </div>

        <div className="text-xs font-mono text-foreground-muted">
          Showing <span className="text-accent-amber font-semibold">{projects.length}</span> published projects
        </div>
      </div>

      {/* Projects Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {projects.map((project) => (
          <ProjectCard key={project.id} project={project} />
        ))}
      </div>
    </main>
  );
}
