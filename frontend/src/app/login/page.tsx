import { AuthForm } from "@/components/AuthForm";
import type { Metadata } from "next";

export const metadata: Metadata = { title: "Entrar" };

export default function LoginPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-[radial-gradient(circle_at_center,#12A2CA,#199BC7,#5A63AB)] px-4">
      <h1 className="mb-6 text-center text-3xl font-bold text-white md:text-4xl">
        Finance App
      </h1>
      <AuthForm mode="login" />
    </main>
  );
}
