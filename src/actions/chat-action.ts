"use server";

import type { BotResponse, SendMessage } from "@/types";
import { cookies } from "next/headers";

type ChatActionState = {
  chatInput: string;
  botResponse: string;
};

export async function chatAction(
  _: ChatActionState,
  formData: FormData,
): Promise<ChatActionState> {
  const input = formData.get("chat-input");
  const question = input?.toString().trim();
  const apiKey = (await cookies()).get("api-key")?.value || "";

  if (!question) return { chatInput: "", botResponse: "" };

  try {
    const apiUrl = process.env.API_URL || "";
    const response = await fetch(`${apiUrl}/finance-ai`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ key: apiKey, question } as SendMessage),
    });

    if (!response.ok) {
      return {
        chatInput: "",
        botResponse: "Desculpe, ocorreu um erro ao processar sua solicitação.",
      };
    }

    const data = (await response.json()) as BotResponse;

    return {
      chatInput: question,
      botResponse: data.message,
    };
  } catch (error) {
    console.error("Erro na requisição:", error);
    return {
      chatInput: "",
      botResponse: "Desculpe, ocorreu um erro ao processar sua solicitação.",
    };
  }
}
