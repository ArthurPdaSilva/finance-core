"use server";
import { cookies } from "next/dist/server/request/cookies";
import { redirect } from "next/navigation";
import { asyncDelay } from "../utils/async-delay";

type AccessActionState = {
  apiKey: string;
  error: string;
};

export async function accessAction(_: AccessActionState, formData: FormData) {
  const apiKey = formData.get("api-key")?.toString().trim() || "";

  await asyncDelay(5000);

  if (!(formData instanceof FormData)) {
    return {
      apiKey: "",
      error: "Dados inválidos",
    };
  }

  if (!apiKey) {
    return {
      apiKey,
      error: "Digite a chave de acesso",
    };
  }

  if (apiKey !== process.env.API_KEY) {
    return {
      apiKey,
      error: "Chave de acesso inválida",
    };
  }

  (await cookies()).set("api-key", apiKey, {
    maxAge: 60 * 60,
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "strict",
  });

  redirect("/chat");
}
