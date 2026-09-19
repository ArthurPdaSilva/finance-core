import { AuthForm } from "@/components/AuthForm";

export default function HomePage() {
  return (
    <div
      className="min-h-screen flex flex-col items-center justify-center px-4
      bg-[radial-gradient(circle_at_center,#12A2CA,#199BC7,#5A63AB)]"
    >
      <h1 className="text-3xl md:text-4xl font-bold text-center text-white mb-6">
        Bem-vindo ao Finance App
      </h1>

      <AuthForm mode="login" />
    </div>
  );
}
