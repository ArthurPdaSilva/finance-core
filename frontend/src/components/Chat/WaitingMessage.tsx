import type { Message } from "@/types";

type WaitingMessageProps = {
  msg: Message;
};

export const WaitingMessage = ({ msg }: WaitingMessageProps) => {
  if (msg.sender !== "waiting") return;

  return (
    <div className="flex items-center gap-2 bg-white p-4 rounded-2xl rounded-tl-none shadow-sm px-4 py-2">
      <div className="w-4 h-4 border-2 border-[#167EAC] border-t-transparent rounded-full animate-spin"></div>
      <p className="text-sm font-medium text-[#167EAC]">{msg.text}</p>
    </div>
  );
};
