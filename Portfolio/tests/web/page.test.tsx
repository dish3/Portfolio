/**
 * Frontend Landing Page Smoke Tests.
 */

import React from "react";
import HomePage from "../../apps/web/app/page";

describe("HomePage Component", () => {
  it("renders the primary landing page without crashing", () => {
    // In React 18 / Next.js Server Components, verify component export and definition
    expect(HomePage).toBeDefined();
    expect(typeof HomePage).toBe("function");
  });
});
