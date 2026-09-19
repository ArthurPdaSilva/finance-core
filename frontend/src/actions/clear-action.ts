"use server";

import { updateTag } from "next/cache";
import { cookies } from "next/headers";

type ClearActionState = {
  error: string;
  success: string;
};

export async function clearAction(
  _: ClearActionState,
  formData: FormData,
): Promise<ClearActionState> {
  if (!(formData instanceof FormData)) {
    return {
      success: "",
      error: "Dados inválidos",
    };
  }

  const sessionToken = (await cookies()).get("session-token")?.value || "";

  if (!sessionToken) {
    return {
      success: "",
      error: "Sessão não encontrada",
    };
  }

  try {
    const apiUrl = process.env.API_URL || "";
    const response = await fetch(`${apiUrl}/finance-ai/chats`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${sessionToken}` },
    });

    if (!response.ok) {
      return {
        error: "Erro ao limpar seus chats",
        success: "",
      };
    }

    updateTag("chat-messages");
    updateTag("chats");

    return {
      error: "",
      success: "Seus chats foram limpos com sucesso!",
    };
  } catch (e) {
    return {
      error: "Erro ao limpar seus chats",
      success: "",
    };
  }
}
