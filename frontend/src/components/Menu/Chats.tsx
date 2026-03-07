import { getChats } from "@/lib/queries";
import Link from "next/link";

export const Chats = async () => {
  const { data } = await getChats();

  return (
    <div className="flex flex-col">
      {data.map(({ id, titulo, criado_em }) => {
        return (
          <Link
            href={`/chat/${id}`}
            key={`${id}-${criado_em}`}
            className="w-full cursor-pointer px-3 py-2 text-gray-600 hover:bg-gray-50 rounded-lg group transition-colors text-sm font-medium text-ellipsis truncate text-left"
          >
            {titulo}
          </Link>
        );
      })}
    </div>
  );
};
