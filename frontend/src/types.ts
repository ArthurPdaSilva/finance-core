export type Message = {
  sender: "user" | "assistant" | "waiting";
  text: string;
};

export type SendMessage = {
  question: string;
  key: string;
  chat_history: string[];
  chat_id?: number;
};

export type BotResponse = {
  message: string;
  chat_id: number;
};

export type Chat = {
  id: number;
  titulo: string;
  criado_em: string;
};

export type MessageHistory = {
  id: number;
  chat_id: number;
  role: "user" | "assistant";
  content: string;
  criado_em: string;
};

export type ChatResponse = {
  status: string;
  count: number;
  data: Chat[];
};

export type MessageResponse = {
  status: string;
  count: number;
  data: MessageHistory[];
};
