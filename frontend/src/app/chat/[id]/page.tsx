import ChatLayout from "@/components/Chat/ChatLayout";
import { getMessages } from "@/lib/queries";
import type { Metadata } from "next";
import { redirect } from "next/navigation";

export const metadata: Metadata = {
  title: "Chat",
};

type ChatIdPageProps = {
  params: Promise<{ id: string }>;
};

export default async function ChatIdPage({ params }: ChatIdPageProps) {
  const { id } = await params;
  const { data } = await getMessages(id);

  if (data.length === 0) {
    redirect("/chat");
  }

  return <ChatLayout history={data} />;
}
