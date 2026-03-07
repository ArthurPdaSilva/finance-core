import { CustomAlertProvider } from "@/components/CustomAlert";
import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "Finance App - Acesso",
    template: "Finance App - %s",
  },
  description:
    "Uma aplicação de chat financeiro construída com Next.js e TypeScript.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt">
      <body className="h-screen">
        {children}
        <CustomAlertProvider />
      </body>
    </html>
  );
}
