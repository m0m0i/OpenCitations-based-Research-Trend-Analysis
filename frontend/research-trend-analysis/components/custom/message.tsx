"use client";

import { motion } from "framer-motion";
import type { ReactNode } from "react";
import { BotIcon, UserIcon } from "./icons";
import { Markdown } from "./markdown";

export const Message = ({
  chatId,
  role,
  content,
}: // toolInvocations,
// attachments,
{
  chatId: string;
  role: string;
  content: string | ReactNode;
  // toolInvocations: Array<ToolInvocation> | undefined;
  // attachments: Array<Attachment>
}) => {
  return (
    <motion.div
      className={`flex flex-row gap-4 px-4 w-full md:w-[500px] md:px-0 first-of-type:pt-20`}
      initial={{ y: 5, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}>
      <div className="size-[24px] border rounded-sm p-1 flex flex-col justify-center items-center shrink-0 text-zinc-500">
        {role === "assistant" ? <BotIcon /> : <UserIcon />}
      </div>
      <div className="flex flex-col gap-2 w-full">
        {content && typeof content === "string" && (
          <div className="text-zinc-800 dark:text-zinc-300 flex flex-col gap-4">
            <Markdown>{content}</Markdown>
          </div>
        )}
      </div>
    </motion.div>
  );
};
