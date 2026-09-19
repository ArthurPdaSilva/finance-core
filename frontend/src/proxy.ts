import { type NextRequest, NextResponse } from "next/server";

export async function proxy(request: NextRequest) {
  const isPublicPage = ["/", "/login", "/signup"].includes(
    request.nextUrl.pathname,
  );
  const isPrivatePage = request.nextUrl.pathname.startsWith("/chat");
  const isGetRequest = request.method === "GET";

  if (!isGetRequest) {
    return NextResponse.next();
  }

  const shouldBeAuthenticated = isPrivatePage && !isPublicPage;
  const shouldBeUnauthenticated = isPublicPage && !isPrivatePage;

  const sessionToken = request.cookies.get("session-token")?.value;
  const isAuthenticated = Boolean(sessionToken);

  if (shouldBeAuthenticated && !isAuthenticated) {
    const publicUrl = new URL("/", request.url);
    return NextResponse.redirect(publicUrl);
  }

  if (shouldBeUnauthenticated && isAuthenticated) {
    const privateUrl = new URL("/chat", request.url);
    return NextResponse.redirect(privateUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: "/:path*",
};
