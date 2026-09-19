"use server";

import { updateTag } from "next/cache";
import { redirect } from "next/navigation";
import { clearSession } from "./auth-action";

export async function logoutAction() {
  await clearSession();
  updateTag("chat-messages");
  updateTag("chats");
  redirect("/");
}
