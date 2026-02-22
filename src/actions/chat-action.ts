"use server";

import type { BotResponse, Message, SendMessage } from "@/types";
import { updateTag } from "next/cache";
import { cookies } from "next/headers";

type ChatActionState = {
  chatInput: string;
  chat_id?: number;
  botResponse: string;
};

export async function chatAction(
  state: ChatActionState,
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
    ...(state.chat_id ? { chat_id: state.chat_id } : {}),
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

    updateTag("chats");

    return {
      chatInput: question,
      botResponse: data.message,
      chat_id: data.chat_id,
    };
  } catch (error) {
    console.error("Erro na requisição:", error);
    return {
      chatInput: "",
      botResponse: "Desculpe, ocorreu um erro ao processar sua solicitação.",
    };
  }
}
