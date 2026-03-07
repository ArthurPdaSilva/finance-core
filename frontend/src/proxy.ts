import { type NextRequest, NextResponse } from "next/server";

export async function proxy(request: NextRequest) {
  const isPublicPage = request.nextUrl.pathname === "/";
  const isPrivatePage = request.nextUrl.pathname.startsWith("/chat");
  const isGetRequest = request.method === "GET";

  if (!isGetRequest) {
    return NextResponse.next();
  }

  const shouldBeAuthenticated = isPrivatePage && !isPublicPage;
  const shouldBeUnauthenticated = isPublicPage && !isPrivatePage;

  const apiKey = request.cookies.get("api-key")?.value;
  const isAuthenticated = apiKey === process.env.API_KEY;

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
