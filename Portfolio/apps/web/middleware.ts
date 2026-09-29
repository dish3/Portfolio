import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { verifyAdminSession } from "./lib/auth";

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Protect all /admin routes
  if (pathname.startsWith("/admin")) {
    const isAuthenticated = verifyAdminSession(request);

    // If unauthenticated and not already on the login skeleton, redirect or set header
    if (!isAuthenticated && !pathname.startsWith("/admin/login")) {
      // In development mode without dev bypass, redirect to login skeleton
      if (process.env.ADMIN_BYPASS_DEV !== "true") {
        const loginUrl = new URL("/admin/login", request.url);
        loginUrl.searchParams.set("from", pathname);
        return NextResponse.redirect(loginUrl);
      }
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/admin/:path*"],
};
