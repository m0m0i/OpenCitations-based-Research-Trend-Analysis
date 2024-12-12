"use client";

import { useTheme } from "next-themes";
import { useEffect, useState } from "react";

import { FiMoon, FiSun } from "react-icons/fi";

export function ThemeToggle() {
  const { setTheme, theme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return null;
  }

  return (
    <div
      className="cursor-pointer"
      onClick={() => {
        setTheme(theme === "dark" ? "light" : "dark");
      }}>
      {theme === "dark" ? (
        <FiSun size={15} onClick={() => setTheme("light")} />
      ) : (
        <FiMoon size={15} onClick={() => setTheme("dark")} />
      )}
    </div>
  );
}
