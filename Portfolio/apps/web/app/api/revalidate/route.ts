import { NextRequest, NextResponse } from "next/server";
import { revalidatePath } from "next/cache";

/**
 * On-Demand ISR Revalidation Endpoint.
 * Sourced from NOVA_05_Frontend_Development_Prompt.md §9 and NOVA_08_Deployment_Prompt.md §4.
 * Triggered by the FastAPI ApprovalService upon human approval of a pending change.
 */
export async function POST(request: NextRequest) {
  const secret = request.nextUrl.searchParams.get("secret");
  const path = request.nextUrl.searchParams.get("path");

  const expectedSecret = process.env.REVALIDATION_SECRET || "development_revalidation_secret";

  if (!secret || secret !== expectedSecret) {
    return NextResponse.json(
      { message: "Invalid revalidation secret" },
      { status: 401 }
    );
  }

  if (!path) {
    return NextResponse.json(
      { message: "Missing 'path' query parameter" },
      { status: 400 }
    );
  }

  try {
    revalidatePath(path);
    return NextResponse.json({
      revalidated: true,
      path,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    return NextResponse.json(
      { message: "Error revalidating path", error: String(error) },
      { status: 500 }
    );
  }
}
