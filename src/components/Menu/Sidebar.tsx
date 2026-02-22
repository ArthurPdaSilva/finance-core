/** biome-ignore-all lint/performance/noImgElement: false positive */
import { useMenu } from "@/MenuContext";
import { fakeChats } from "@/utils/fake-chat";
import { LogoutButton } from "./LogoutButton";

export const Sidebar = () => {
  const { isOpen, toggleMenu } = useMenu();

  return (
    <aside
      className={`
        fixed inset-y-0 left-0 z-50 w-72 bg-white border-r border-gray-200 flex flex-col shrink-0
        transition-transform duration-300 ease-in-out
        md:static md:translate-x-0 md:w-64
        ${isOpen ? "translate-x-0" : "-translate-x-full"}
      `}
    >
      <div className="h-16 flex items-center justify-between px-6 border-b border-gray-50/50">
        <div className="flex items-center gap-2">
          <img src="/logo.png" alt="Logo" className="w-8 h-8" />
          <span className="font-bold text-lg tracking-tight">Finance AI</span>
        </div>
        <button
          type="button"
          onClick={toggleMenu}
          className="md:hidden p-1 text-gray-400 hover:text-gray-600"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
            className="w-6 h-6"
          >
            <title>Close</title>
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M6 18 18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>

      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        <button
          type="button"
          className="w-full cursor-pointer flex items-center gap-3 px-3 py-2 text-white rounded-lg group shadow-sm shadow-blue-200
            bg-[radial-gradient(circle_at_center,#12A2CA,#199BC7,#5A63AB)]"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth="1.5"
            stroke="currentColor"
            className="w-5 h-5"
          >
            <title>AI CHAT</title>
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M8.625 9.75a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H8.25m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H12m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0h-.375m-13.5 3.01c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 0 1 .865-.501 48.172 48.172 0 0 0 3.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0 0 12 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018Z"
            />
          </svg>
          <span className="text-sm font-medium">AI Chat</span>
        </button>

        <button
          type="button"
          className="w-full cursor-pointer flex items-center gap-3 px-3 py-2 text-gray-600 hover:bg-gray-50 rounded-lg group transition-colors"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth="1.5"
            stroke="currentColor"
            className="w-5 h-5"
          >
            <title>Novo chat</title>
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
          </svg>
          <span className="text-sm font-medium">Novo chat</span>
        </button>

        <div className="pt-4 mt-4 border-t border-gray-100">
          <span className="px-3 text-xs font-semibold text-gray-400 uppercase tracking-wider">
            Chats
          </span>
          <div className="flex flex-col">
            {fakeChats.map(({ id, title }) => {
              return (
                <button
                  key={id}
                  type="button"
                  className="w-full cursor-pointer px-3 h-14 text-gray-600 hover:bg-gray-50 rounded-lg group transition-colors text-sm font-medium text-ellipsis truncate text-left"
                >
                  {title}
                </button>
              );
            })}
          </div>
        </div>

        <div className="pt-4 mt-4 border-t border-gray-100">
          <span className="px-3 text-xs font-semibold text-gray-400 uppercase tracking-wider">
            Configurações
          </span>
          <LogoutButton />
        </div>
      </nav>

      {/* PERFIL DO USUÁRIO */}
      <div className="p-4 border-t border-gray-200">
        <div className="flex items-center gap-3">
          <div className="bg-[linear-gradient(90deg,#12A2CA,#199BC7,#5A63AB)] w-10 h-10 rounded-full flex items-center justify-center text-white text-sm font-medium shrink-0">
            AU
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-gray-900 truncate">
              Usuário Admin
            </p>
            <p className="text-xs text-gray-500 truncate">Usuário único</p>
          </div>
        </div>
      </div>
    </aside>
  );
};
