import ChatLayout from "@/components/Chat/ChatLayout";
import { getMessages } from "@/lib/queries";
import type { Metadata } from "next";
import { redirect } from "next/navigation";

export const metadata: Metadata = {
  title: "Chat",
};

type ChatIdPageProps = {
  params: Promise<{ token: string }>;
};


export default async function ChatIdPage({ params }: ChatIdPageProps) {
  const { token } = await params;
  const { data } = await getMessages(token);

  if (data.length === 0) {
    redirect("/chat");
  }

  return <ChatLayout history={data} />;
}
