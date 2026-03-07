"use client";
import { clearAction } from "@/actions/clear-action";
import { useRouter } from "next/navigation";
import { useActionState, useEffect } from "react";
import { CustomAlert } from "../CustomAlert";

export const ClearButton = () => {
  const initialState = {
    error: "",
    success: "",
  };
  const [state, action, isPending] = useActionState(clearAction, initialState);
  const router = useRouter();

  useEffect(() => {
    if (isPending) {
      CustomAlert.info("Limpando banco...", false);
      return;
    }

    CustomAlert.dismiss();
    if (state.error) {
      CustomAlert.error(state.error);
      return;
    }

    if (state.success) {
      CustomAlert.success(state.success);
      router.push("/chat");
      return;
    }
  }, [state, isPending, router.push]);

  return (
    <form action={action}>
      <button
        type="submit"
        className="flex w-full cursor-pointer items-center gap-3 px-3 py-2 mt-2 text-gray-600 hover:bg-gray-50 rounded-lg group transition-colors"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth={1.5}
          stroke="currentColor"
          className="w-5 h-5 text-gray-400 group-hover:text-gray-600"
        >
          <title>Clear</title>
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673A2.25 2.25 0 0 1 15.916 21.75H8.084A2.25 2.25 0 0 1 5.84 19.673L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .563c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.479-.398m7.5 0v-.916c0-.983-.895-1.75-2-1.75h-3.5c-1.105 0-2 .767-2 1.75V5.03"
          />
        </svg>
        <span className="text-sm font-medium">Limpar Dados</span>
      </button>
    </form>
  );
};
