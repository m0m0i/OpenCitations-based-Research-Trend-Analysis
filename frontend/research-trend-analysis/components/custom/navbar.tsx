import Image from "next/image";
import { ThemeToggle } from "./theme-toggle";

export const Navbar = async () => {
  return (
    <>
      <div className="bg-backgrond absolute top-0 left-0 w-dvw py-2 px-3 justify-between flex flex-row items-center z-30">
        <div className="flex flex-row gap-3 items-center">
          <div className="flex flex-row gap-2 items-center">
            <div className="text-sm dark:text-zinc-300 truncate w-28 md:w-fit">
              Research Trend Analysis
            </div>
          </div>
        </div>
        <ThemeToggle />
      </div>
    </>
  );
};
