/** biome-ignore-all lint/suspicious/noArrayIndexKey: false positive */
/** biome-ignore-all lint/correctness/useExhaustiveDependencies: false positive */
"use client";
import { useMessage } from "@/contexts/MessageContext";
import type { Message, MessageHistory } from "@/types";
import { useEffect, useRef } from "react";
import { InteractionMessage } from "./InteractionMessage";
import { WaitingMessage } from "./WaitingMessage";

type MessagesProps = {
  history?: MessageHistory[];
};

export const Messages = ({ history = [] }: MessagesProps) => {
  const { messages, setMessages } = useMessage();
  const messagesRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (history.length > 0) {
      const messages: Message[] = history.map((message) => {
        return {
          text: message.content,
          sender: message.role,
        };
      });

      setMessages(messages);
    }
  }, [history]);

  useEffect(() => {
    const div = messagesRef.current;
    if (!div) return;

    div.scrollTo({
      top: div.scrollHeight,
      behavior: "smooth",
    });
  }, [messages]);

  return (
    <div
      ref={messagesRef}
      className="bg-gray-200 flex h-[80vh] overflow-y-auto p-4 rounded-xl flex-col-reverse shadow-inner"
    >
      <div className="w-full max-w-4xl mx-auto flex flex-col-reverse gap-4">
        {messages.length === 0 && (
          <div className="flex self-start max-w-[80%] md:max-w-[60%] bg-white p-4 rounded-2xl rounded-tl-none shadow-sm">
            <p className="text-sm md:text-base font-medium text-gray-700">
              Olá! Eu sou o Finance Bot e estou aqui para te ajudar com suas
              finanças :)
            </p>
          </div>
        )}

        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex w-full ${
              msg.sender === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <WaitingMessage msg={msg} />
            <InteractionMessage msg={msg} />
          </div>
        ))}
      </div>
    </div>
  );
};
