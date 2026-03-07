"use client";
import { createContext, useContext, useState } from "react";
import type { Message } from "../types";

type MessageContext = {
  messages: Message[];
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>;
};

const MessageContext = createContext<MessageContext | null>(null);

export function MessagesProvider({ children }: { children: React.ReactNode }) {
  const [messages, setMessages] = useState<Message[]>([]);

  return (
    <MessageContext.Provider value={{ messages, setMessages }}>
      {children}
    </MessageContext.Provider>
  );
}

export function useMessage() {
  const ctx = useContext(MessageContext);
  if (!ctx)
    throw new Error("useMessage deve ser usado dentro de MessagesProvider");
  return ctx;
}
