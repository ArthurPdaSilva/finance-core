"use server";

import type { BotResponse, Message, SendMessage } from "@/types";
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
  const messages = formData.get("messages")?.toString() || "";
  const question = input?.toString().trim();
  const apiKey = (await cookies()).get("api-key")?.value || "";

  if (!question) return { chatInput: "", botResponse: "" };
  const chatHistory = messages
    ? (JSON.parse(messages) as Message[]).reverse()
    : [];

  const chatHistoryStrings = chatHistory.map(
    (msg) => `${msg.sender}: ${msg.text}`,
  );

  const sendMessage: SendMessage = {
    question,
    key: apiKey,
    chat_history: chatHistoryStrings,
  };

  try {
    const apiUrl = process.env.API_URL || "";
    const response = await fetch(`${apiUrl}/finance-ai`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(sendMessage),
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
