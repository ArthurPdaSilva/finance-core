"use client";
import { MenuProvider } from "@/contexts/MenuContext";
import { MobileMenu } from "./MobileMenu";
import { Overlay } from "./Overlay";
import { Sidebar } from "./Sidebar";

type MenuContainerProps = {
  children: React.ReactNode;
};

export const MenuContainer = ({ children }: MenuContainerProps) => {
  return (
    <MenuProvider>
      <MobileMenu />
      <Overlay />
      <Sidebar>{children}</Sidebar>
    </MenuProvider>
  );
};
