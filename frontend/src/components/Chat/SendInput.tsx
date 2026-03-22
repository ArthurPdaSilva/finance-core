/** biome-ignore-all lint/correctness/useExhaustiveDependencies: false positive */
"use client";

import { chatAction } from "@/actions/chat-action";
import { useMessage } from "@/contexts/MessageContext";
import { usePathname, useRouter } from "next/navigation";
import { useActionState, useEffect, useRef, useState } from "react";

export const SendInput = () => {
  const { messages, setMessages } = useMessage();
  const [inputValue, setInputValue] = useState("");
  const pathname = usePathname();
  const router = useRouter();
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const [, base, token] = pathname.split("/");

  const initialState = {
    chatInput: "",
    botResponse: "",
    token: base === "chat" && token ? String(token) : undefined,
  };
  const [state, action, isPending] = useActionState(chatAction, initialState);

  useEffect(() => {
    if (state.token && pathname === "/chat" && !token) {
      const newUrl = `${pathname}/${state.token}`;
      router.replace(newUrl);
    }
  }, [state.token, pathname]);

  useEffect(() => {
    if (isPending) {
      setMessages((prev) => [
        { sender: "waiting", text: "O Finance Bot está pensando..." },
        { sender: "user", text: inputValue },
        ...prev.filter((m) => m.sender !== "waiting"),
      ]);
    }

    if (!isPending) {
      setInputValue("");
    }
  }, [isPending, state.botResponse]);

  return (
    <form
      action={action}
      id="form"
      onClick={() => inputRef.current?.focus()}
      onKeyDown={() => inputRef.current?.focus()}
      className=" w-[80vw] md:w-[40vw]  flex items-end gap-4 m-auto rounded-xl border-[#2A4A7A] bg-[#0F1A2A]/40 px-5 py-4"
    >
      <input type="hidden" name="messages" value={JSON.stringify(messages)} />

      <textarea
        ref={inputRef}
        id="input"
        name="chat-input"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        disabled={isPending}
        rows={1}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            (
              document.getElementById("form") as HTMLFormElement
            )?.requestSubmit();
          }
        }}
        placeholder="Digite sua pergunta.."
        className={`flex-1 resize-none bg-transparent outline-none text-base leading-relaxed placeholder-white/40 text-white ${isPending && "opacity-50 cursor-not-allowed"} p-1`}
      ></textarea>
      <button
        disabled={isPending || !inputValue.trim()}
        type="submit"
        className={`flex items-center justify-center w-10 h-10 rounded-full bg-[linear-gradient(90deg,#12A2CA,#199BC7,#5A63AB)] text-white text-sm font-medium ${isPending || !inputValue.trim() ? "cursor-not-allowed opacity-50" : "cursor-pointer"}`}
      >
        {isPending ? (
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            fill="currentColor"
          >
            <title>Carregando...</title>
            <rect x="4" y="4" width="12" height="12" rx="3"></rect>
          </svg>
        ) : (
          <svg
            width="20"
            height="20"
            viewBox="0 0 20 20"
            fill="currentColor"
            xmlns="http://www.w3.org/2000/svg"
          >
            <title>Enviar mensagem</title>
            <path
              d="M10 4L10 16"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
            />
            <path
              d="M6 8L10 4L14 8"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        )}
      </button>
    </form>
  );
};
