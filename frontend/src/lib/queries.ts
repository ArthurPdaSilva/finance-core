"use server";

import type { ChatResponse, MessageResponse } from "@/types";
import { cookies } from "next/headers";
import { notFound } from "next/navigation";

export async function getChats(): Promise<ChatResponse> {
  const apiKey = (await cookies()).get("api-key")?.value || "";

  const urlSafeKey = encodeURIComponent(apiKey);
  const res = await fetch(
    `${process.env.API_URL}/finance-ai/chats?key=${urlSafeKey}`,
    {
      method: "GET",
      next: {
        tags: ["chats"],
        revalidate: Number(1800),
      },
    },
  );

  if (res.status === 404) notFound();
  const json = await res.json();
  return json;
}

export async function getMessages(token: string): Promise<MessageResponse> {
  const apiKey = (await cookies()).get("api-key")?.value || "";
  const urlSafeKey = encodeURIComponent(apiKey);

  const res = await fetch(
    `${process.env.API_URL}/finance-ai/messages?key=${urlSafeKey}&token=${token}`,
    {
      method: "GET",
      next: {
        tags: ["chat-messages", `chats-message-${token}`],
        revalidate: Number(1800),
      },
    },
  );

  if (res.status === 404) notFound();
  const json = await res.json();
  return json;
}
