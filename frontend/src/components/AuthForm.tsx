"use client";

import { loginAction, signupAction } from "@/actions/auth-action";
import Link from "next/link";
import { useActionState } from "react";

type AuthFormProps = {
  mode: "login" | "signup";
};

const initialState = { email: "", name: "", error: "" };

export function AuthForm({ mode }: AuthFormProps) {
  const [state, action, isPending] = useActionState(
    mode === "login" ? loginAction : signupAction,
    initialState,
  );
  const isSignup = mode === "signup";

  return (
    <form
      action={action}
      className="flex w-full max-w-sm flex-col gap-4 rounded-xl border border-[#24385B] bg-[#0F1A2A]/90 p-6 text-left shadow-lg backdrop-blur-sm"
    >
      <div>
        <h2 className="text-xl font-semibold text-white">
          {isSignup ? "Criar conta" : "Entrar"}
        </h2>
        <p className="mt-1 text-sm text-slate-300">
          {isSignup
            ? "Crie seu acesso para salvar seus chats."
            : "Acesse seus chats financeiros."}
        </p>
      </div>

      {isSignup && (
        <label className="flex flex-col gap-1 text-sm text-slate-200">
          Nome
          <input
            name="name"
            defaultValue={state.name}
            disabled={isPending}
            required
            autoComplete="name"
            className="rounded-md border border-[#2A4A7A] bg-[#0F1A2A]/60 p-2 text-white outline-none focus:border-[#12A2CA]"
          />
        </label>
      )}

      <label className="flex flex-col gap-1 text-sm text-slate-200">
        Email
        <input
          name="email"
          defaultValue={state.email}
          disabled={isPending}
          required
          type="email"
          autoComplete="email"
          className="rounded-md border border-[#2A4A7A] bg-[#0F1A2A]/60 p-2 text-white outline-none focus:border-[#12A2CA]"
        />
      </label>

      <label className="flex flex-col gap-1 text-sm text-slate-200">
        Senha
        <input
          name="password"
          disabled={isPending}
          required
          minLength={8}
          type="password"
          autoComplete={isSignup ? "new-password" : "current-password"}
          className="rounded-md border border-[#2A4A7A] bg-[#0F1A2A]/60 p-2 text-white outline-none focus:border-[#12A2CA]"
        />
      </label>

      {state.error && (
        <p className="rounded border border-red-500/30 bg-red-500/10 p-2 text-sm text-red-100">
          {state.error}
        </p>
      )}

      <button
        disabled={isPending}
        type="submit"
        className="rounded-md bg-[#167EAC] p-2 font-medium text-white transition-colors hover:bg-[#199BC7] disabled:cursor-wait disabled:opacity-70"
      >
        {isPending ? "Aguarde..." : isSignup ? "Criar conta" : "Entrar"}
      </button>

      <Link
        href={isSignup ? "/login" : "/signup"}
        className="text-center text-sm text-cyan-200 hover:text-white"
      >
        {isSignup ? "Já tenho uma conta" : "Ainda não tenho uma conta"}
      </Link>
    </form>
  );
}
