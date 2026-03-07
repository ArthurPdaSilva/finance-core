import ChatLayout from "@/components/Chat/ChatLayout";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Chat",
};

export default async function ChatPage() {
  return <ChatLayout />;
}
