/**
 * Admin Dashboard Route & Component Tests.
 */

import AdminDashboardPage from "../../apps/web/app/admin/page";
import PendingApprovalsPage from "../../apps/web/app/admin/pending/page";
import AdminProjectsPage from "../../apps/web/app/admin/projects/page";
import AdminConnectorsPage from "../../apps/web/app/admin/connectors/page";
import { verifyAdminSession } from "../../apps/web/lib/auth";

describe("Admin Dashboard Pages", () => {
  it("exports valid React components for all admin routes", () => {
    expect(typeof AdminDashboardPage).toBe("function");
    expect(typeof PendingApprovalsPage).toBe("function");
    expect(typeof AdminProjectsPage).toBe("function");
    expect(typeof AdminConnectorsPage).toBe("function");
  });

  it("authenticates requests with valid admin cookie or token", () => {
    const mockRequestWithCookie = {
      cookies: {
        get: (name: string) => (name === "nova_admin_session" ? { value: "valid_session" } : undefined),
      },
      headers: {
        get: () => null,
      },
    } as any;

    expect(verifyAdminSession(mockRequestWithCookie)).toBe(true);

    const mockUnauthenticatedRequest = {
      cookies: {
        get: () => undefined,
      },
      headers: {
        get: () => null,
      },
    } as any;

    expect(verifyAdminSession(mockUnauthenticatedRequest)).toBe(false);
  });
});
