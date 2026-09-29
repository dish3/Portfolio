/**
 * Projects Page and ProjectCard Tests.
 */

import React from "react";
import ProjectsPage from "../../apps/web/app/projects/page";
import ProjectDetailPage from "../../apps/web/app/projects/[slug]/page";
import { ProjectCard } from "../../apps/web/components/projects/project-card";
import { Project } from "@nova/types";

describe("Projects Components", () => {
  const mockProject: Project = {
    id: "test-id",
    slug: "test-project",
    title: "Test Project",
    short_description: "Short description for testing",
    long_description: "Long description for testing",
    source: "github",
    github_repo_url: "https://github.com/disha/test",
    live_demo_url: "https://test.dev",
    drive_fallback_url: null,
    linkedin_post_url: null,
    youtube_video_url: null,
    cover_image_url: null,
    tech_stack: ["Python", "FastAPI"],
    status: "published",
    started_at: "2026-01-01",
    updated_at: "2026-01-02",
  };

  it("exports valid React server components", () => {
    expect(typeof ProjectsPage).toBe("function");
    expect(typeof ProjectDetailPage).toBe("function");
  });

  it("exports ProjectCard component", () => {
    expect(typeof ProjectCard).toBe("function");
  });
});
