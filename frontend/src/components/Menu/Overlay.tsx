/** biome-ignore-all lint/a11y/useKeyWithClickEvents: false positive */
/** biome-ignore-all lint/a11y/noStaticElementInteractions: false positive */

import { useMenu } from "@/contexts/MenuContext";

export const Overlay = () => {
  const { isOpen, toggleMenu } = useMenu();

  return (
    <div
      className={`fixed inset-0 bg-black/40 z-40 transition-opacity duration-300 md:hidden ${
        isOpen ? "opacity-100 visible" : "opacity-0 invisible"
      }`}
      onClick={toggleMenu}
    />
  );
};
