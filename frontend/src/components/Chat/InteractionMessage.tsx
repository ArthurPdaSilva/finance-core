import type { Message } from "@/types";
import { MarkdownRenderer } from "./MarkdownRenderer";

type InteractionMessageProps = {
  msg: Message;
};

export const InteractionMessage = ({ msg }: InteractionMessageProps) => {
  if (msg.sender === "waiting") return;

  return (
    <div
      className={`max-w-[85%] p-3 px-4 shadow-md transition-all ${
        msg.sender === "user"
          ? "bg-[#167EAC] text-white rounded-2xl rounded-tr-none"
          : "bg-white text-black rounded-2xl rounded-tl-none"
      }`}
    >
      <div className="prose prose-sm max-w-none">
        <MarkdownRenderer markdown={msg.text} />
      </div>
    </div>
  );
};
