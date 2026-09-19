"use server";

import { cookies } from "next/headers";
import { redirect } from "next/navigation";

const sessionCookie = "session-token";

type AuthState = {
  email: string;
  name?: string;
  error: string;
};

async function authenticate(path: string, body: Record<string, string>) {
  const response = await fetch(`${process.env.API_URL}/auth/${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const data = (await response.json().catch(() => null)) as {
      detail?: string;
    } | null;
    return { error: data?.detail || "Não foi possível autenticar." };
  }

  const data = (await response.json()) as { token: string };
  (await cookies()).set(sessionCookie, data.token, {
    httpOnly: true,
    maxAge: 60 * 60 * 24 * 7,
    path: "/",
    sameSite: "lax",
    secure: process.env.NODE_ENV === "production",
  });

  return null;
}

export async function loginAction(
  _state: AuthState,
  formData: FormData,
): Promise<AuthState> {
  const email = formData.get("email")?.toString().trim() || "";
  const password = formData.get("password")?.toString() || "";
  const error = await authenticate("login", { email, password });

  if (error) return { email, error: error.error };
  redirect("/chat");
}

export async function signupAction(
  _state: AuthState,
  formData: FormData,
): Promise<AuthState> {
  const name = formData.get("name")?.toString().trim() || "";
  const email = formData.get("email")?.toString().trim() || "";
  const password = formData.get("password")?.toString() || "";
  const error = await authenticate("signup", { name, email, password });

  if (error) return { name, email, error: error.error };
  redirect("/chat");
}

export async function clearSession() {
  const token = (await cookies()).get(sessionCookie)?.value;
  if (token) {
    await fetch(`${process.env.API_URL}/auth/logout`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
    }).catch(() => undefined);
  }
  (await cookies()).delete(sessionCookie);
}
