"use server";

import type { AuthUser, ChatResponse, MessageResponse } from "@/types";
import { cookies } from "next/headers";
import { notFound, redirect } from "next/navigation";

export async function getCurrentUser(): Promise<AuthUser> {
  const sessionToken = (await cookies()).get("session-token")?.value || "";
  const res = await fetch(`${process.env.API_URL}/auth/me`, {
    headers: { Authorization: `Bearer ${sessionToken}` },
    cache: "no-store",
  });

  if (res.status === 401) redirect("/login");
  if (!res.ok) throw new Error("Não foi possível carregar o usuário.");
  return (await res.json()) as AuthUser;
}

export async function getChats(): Promise<ChatResponse> {
  const sessionToken = (await cookies()).get("session-token")?.value || "";
  const res = await fetch(`${process.env.API_URL}/finance-ai/chats`, {
    method: "GET",
    headers: { Authorization: `Bearer ${sessionToken}` },
    next: {
      tags: ["chats"],
      revalidate: Number(1800),
    },
  });

  if (res.status === 401) redirect("/login");
  if (res.status === 404) notFound();
  const json = await res.json();
  return json;
}

export async function getMessages(token: string): Promise<MessageResponse> {
  const sessionToken = (await cookies()).get("session-token")?.value || "";

  const res = await fetch(
    `${process.env.API_URL}/finance-ai/messages?chat_token=${encodeURIComponent(token)}`,
    {
      method: "GET",
      headers: { Authorization: `Bearer ${sessionToken}` },
      next: {
        tags: ["chat-messages", `chats-message-${token}`],
        revalidate: Number(1800),
      },
    },
  );

  if (res.status === 401) redirect("/login");
  if (res.status === 404) notFound();
  const json = await res.json();
  return json;
}
