export type Message = {
  sender: "user" | "bot" | "waiting";
  text: string;
};

export type SendMessage = {
  question: string;
  key: string;
  chat_history: string[];
};

export type BotResponse = {
  message: string;
};
