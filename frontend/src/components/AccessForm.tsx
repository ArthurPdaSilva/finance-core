"use client";
import { accessAction } from "@/actions/access-action";
import { useActionState, useEffect } from "react";
import { CustomAlert } from "./CustomAlert";

export const AccessForm = () => {
  const initialState = {
    apiKey: "",
    error: "",
  };
  const [state, action, isPending] = useActionState(accessAction, initialState);

  useEffect(() => {
    if (state.error) {
      CustomAlert.dismiss();
      CustomAlert.error(state.error);
    }
  }, [state]);

  return (
    <form
      className="flex flex-col gap-3 w-full max-w-sm text-center p-6 rounded-xl
  bg-[#0F1A2A]/90 border border-[#24385B] shadow-lg backdrop-blur-sm"
      action={action}
    >
      <input
        defaultValue={state.apiKey}
        disabled={isPending}
        type="text"
        id="api-key"
        name="api-key"
        placeholder="Digite a chave de acesso"
        className="border border-[#2A4A7A] bg-[#0F1A2A]/60 text-white rounded-md p-2
      placeholder-gray-300 focus:border-[#12A2CA] outline-none transition"
      />

      <button
        disabled={isPending}
        type="submit"
        className="bg-[#167EAC] hover:bg-[#199BC7] text-white rounded-md p-2
    transition-colors duration-300 cursor-pointer font-medium"
      >
        {isPending ? "Validando..." : "Acessar"}
      </button>
      {state.error && (
        <div className="mt-2 p-2 rounded border border-red-500/30 bg-red-500/10 text-red-100">
          {state.error}
        </div>
      )}
    </form>
  );
};
