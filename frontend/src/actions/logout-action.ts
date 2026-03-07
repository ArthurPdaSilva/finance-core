"use server";

import { updateTag } from "next/cache";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";

export async function logoutAction() {
  (await cookies()).delete("api-key");
  updateTag("chat-messages");
  updateTag("chats");
  redirect("/");
}
