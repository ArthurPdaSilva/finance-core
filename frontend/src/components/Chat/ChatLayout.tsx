import { ChatContainer } from "@/components/Chat/ChatContainer";
import { Messages } from "@/components/Chat/Messages";
import { SendInput } from "@/components/Chat/SendInput";
import { Menu } from "@/components/Menu";
import { MessagesProvider } from "@/contexts/MessageContext";
import type { MessageHistory } from "@/types";

type ChatLayoutProps = {
  history?: MessageHistory[];
};

export default async function ChatLayout({ history = [] }: ChatLayoutProps) {
  return (
    <div className="h-full flex flex-col md:flex-row">
      <Menu />
      <ChatContainer>
        <MessagesProvider>
          <Messages history={history} />
          <SendInput />
        </MessagesProvider>
      </ChatContainer>
    </div>
  );
}
