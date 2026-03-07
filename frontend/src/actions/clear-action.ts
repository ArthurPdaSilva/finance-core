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

  const apiKey = (await cookies()).get("api-key")?.value || "";

  if (!apiKey) {
    return {
      success: "",
      error: "Chave de acesso não encontrada",
    };
  }

  try {
    const apiUrl = process.env.API_URL || "";
    const response = await fetch(`${apiUrl}/init-db`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ key: apiKey }),
    });

    if (!response.ok) {
      return {
        error: "Erro ao limpar o banco de dados",
        success: "",
      };
    }

    updateTag("chat-messages");
    updateTag("chats");

    return {
      error: "",
      success: "Banco de dados limpado com sucesso!",
    };
  } catch (e) {
    console.log(e);
    return {
      error: "Erro ao limpar o banco de dados",
      success: "",
    };
  }
}
