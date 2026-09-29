import React from "react";
import Link from "next/link";
import { notFound } from "next/navigation";
import {
  ArrowLeft,
  Github,
  Globe,
  HardDrive,
  Calendar,
  MessageSquare,
  Sparkles,
  Share2,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { ApiClient } from "@/lib/api-client";
import { Project } from "@nova/types";

interface ProjectDetailPageProps {
  params: {
    slug: string;
  };
}

export const revalidate = 3600; // On-demand ISR revalidation

export default async function ProjectDetailPage({ params }: ProjectDetailPageProps) {
  const { slug } = params;
  let project: Project | null = null;

  try {
    project = await ApiClient.getProjectBySlug(slug);
  } catch (error) {
    if (slug === "nova-ai-portfolio-os") {
      project = {
        id: "e4a2c1b0-9876-4321-b012-3456789abcde",
        slug: "nova-ai-portfolio-os",
        title: "NOVA AI Portfolio OS",
        short_description: "An autonomous AI-managed Operating System and story-driven portfolio built with Next.js 14 and FastAPI.",
        long_description: (
          "NOVA is an autonomous personal operating system designed to continuously ingest developer activity " +
          "across GitHub, LeetCode, and LinkedIn. It uses Gemini AI models to draft project descriptions and updates, " +
          "which are routed through a human approval queue before publication into a PostgreSQL + pgvector knowledge graph.\n\n" +
          "The public presentation features a Quiet Intelligence dark observatory theme, on-demand ISR revalidation, " +
          "and strict security isolation keeping all LLM keys and service secrets server-side."
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
      };
    }
  }

  if (!project) {
    notFound();
  }

  return (
    <article className="min-h-screen py-16 px-6 max-w-4xl mx-auto">
      {/* Back Link */}
      <Link
        href="/projects"
        className="inline-flex items-center gap-1.5 text-xs font-mono text-foreground-muted hover:text-accent-amber mb-8 transition-colors"
      >
        <ArrowLeft className="w-3.5 h-3.5" />
        <span>Back to Projects Archive</span>
      </Link>

      {/* Hero Header */}
      <header className="space-y-4 border-b border-border pb-8">
        <div className="flex flex-wrap items-center gap-2">
          <Badge variant="amber">
            <Sparkles className="w-3 h-3" />
            <span>AI Knowledge Graph Verified</span>
          </Badge>
          <Badge variant="default" className="capitalize">
            Source: {project.source}
          </Badge>
          {project.started_at && (
            <div className="flex items-center gap-1 text-xs font-mono text-foreground-muted ml-auto">
              <Calendar className="w-3.5 h-3.5" />
              <span>Started: {project.started_at}</span>
            </div>
          )}
        </div>

        <h1 className="text-3xl sm:text-5xl font-extrabold font-mono text-foreground tracking-tight">
          {project.title}
        </h1>

        <p className="text-lg text-foreground-secondary leading-relaxed font-sans">
          {project.short_description}
        </p>

        {/* Action Button Links */}
        <div className="flex flex-wrap items-center gap-3 pt-4">
          {project.github_repo_url && (
            <a
              href={project.github_repo_url}
              target="_blank"
              rel="noopener noreferrer"
            >
              <Button variant="secondary" size="sm" className="gap-2">
                <Github className="w-4 h-4" />
                <span>GitHub Repository</span>
              </Button>
            </a>
          )}

          {project.live_demo_url ? (
            <a
              href={project.live_demo_url}
              target="_blank"
              rel="noopener noreferrer"
            >
              <Button variant="primary" size="sm" className="gap-2">
                <Globe className="w-4 h-4" />
                <span>Live Demo</span>
              </Button>
            </a>
          ) : project.drive_fallback_url ? (
            <a
              href={project.drive_fallback_url}
              target="_blank"
              rel="noopener noreferrer"
            >
              <Button variant="secondary" size="sm" className="gap-2">
                <HardDrive className="w-4 h-4" />
                <span>Drive Demo Fallback</span>
              </Button>
            </a>
          ) : null}
        </div>
      </header>

      {/* Tech Stack Badges */}
      <section className="py-6 border-b border-border">
        <h2 className="text-xs font-mono uppercase tracking-wider text-foreground-muted mb-3">
          Technologies & Competencies
        </h2>
        <div className="flex flex-wrap gap-2">
          {project.tech_stack.map((tech) => (
            <Badge key={tech} variant="ice" className="py-1 px-3">
              {tech}
            </Badge>
          ))}
        </div>
      </section>

      {/* AI Synthesized Deep Description */}
      <section className="py-8 space-y-4">
        <h2 className="text-sm font-mono uppercase tracking-wider text-accent-amber">
          System Architecture & Implementation
        </h2>
        <div className="prose prose-invert max-w-none text-foreground-secondary leading-relaxed space-y-4 font-sans text-base">
          {project.long_description?.split("\n\n").map((para, idx) => (
            <p key={idx}>{para}</p>
          ))}
        </div>
      </section>

      {/* Ask AI About This Project Card (Deep-link to Chat Agent) */}
      <section className="pt-6">
        <Card accent="amber" className="bg-surface/50">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="space-y-1">
              <div className="flex items-center gap-2 text-accent-amber font-mono text-sm font-semibold">
                <MessageSquare className="w-4 h-4" />
                <span>Ask NOVA AI About This Project</span>
              </div>
              <p className="text-xs text-foreground-secondary">
                The persistent Chat Agent has indexed the repository commits, tech stack, and documentation for &quot;{project.title}&quot;.
              </p>
            </div>
            <Link href={`/?ask=${encodeURIComponent(`Tell me about ${project.title}`)}`}>
              <Button variant="secondary" size="sm" className="whitespace-nowrap">
                Query Project Memory
              </Button>
            </Link>
          </div>
        </Card>
      </section>
    </article>
  );
}
