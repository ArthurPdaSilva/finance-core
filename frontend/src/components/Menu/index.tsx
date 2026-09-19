import { Chats } from "./Chats";
import { MenuContainer } from "./MenuContainer";
import { getCurrentUser } from "@/lib/queries";

export const Menu = async () => {
  const user = await getCurrentUser();

  return (
    <MenuContainer user={user}>
      <Chats />
    </MenuContainer>
  );
};
