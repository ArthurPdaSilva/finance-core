"use client";
import { MenuProvider } from "@/contexts/MenuContext";
import type { AuthUser } from "@/types";
import { MobileMenu } from "./MobileMenu";
import { Overlay } from "./Overlay";
import { Sidebar } from "./Sidebar";

type MenuContainerProps = {
  children: React.ReactNode;
  user: AuthUser;
};

export const MenuContainer = ({ children, user }: MenuContainerProps) => {
  return (
    <MenuProvider>
      <MobileMenu />
      <Overlay />
      <Sidebar user={user}>{children}</Sidebar>
    </MenuProvider>
  );
};
