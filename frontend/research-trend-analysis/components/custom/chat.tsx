"use client";

import { Message as PreviewMessage } from "@/components/custom/message";
import { Message } from "ai";
import { motion } from "framer-motion";
import { useState } from "react";
import { v4 as uuidv4 } from "uuid";
import { UserInput } from "./input";
import { Overview } from "./overview";
import { useScrollToBottom } from "./use_scroll-to-bottom";

const suggestedActions = [
  {
    title: "How many ",
    label: "publications?",
    action: "How many publications were authored in 2016?",
  },
  {
    title: "Find the article",
    label: "about oxidative stress",
    action:
      "find articles about oxidative stress. Return the title of the most relevant article",
  },
];

export function Chat({
  id,
  initialMessages,
}: {
  id: string;
  initialMessages: Array<Message>;
}) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (event?: { preventDefault?: () => void }) => {
    event?.preventDefault && event.preventDefault();

    const id = uuidv4();
    setIsLoading(true);

    setMessages((prevMessages) => [
      ...prevMessages,
      { id: id, role: "user", content: input },
    ]);

    // If http://localhost:5001/ or http://127.0.0.1/5001/ does not work,
    // chenge the url to the IP address below "Running on http://127.0.0.1:5001"
    // that you can find when you run flask at the backend,
    const url = "http://192.168.10.20:5001/";

    try {
      setInput("");
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          id: id,
          role: "user",
          content: input,
        }),
      });

      if (!response.ok) {
        const errorData = await response.text();
        console.error("API request failed:", response.status, errorData);
      }

      const json = await response.json();
      console.log("Response from server:", json);

      const res: Message = {
        id: json.id,
        role: json.role,
        content: json.content,
        createdAt: json.created_at,
      };

      setMessages((prevMessages) => [...prevMessages, res]);
      setIsLoading(false);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const append = (suggestedAction: string) => {
    setInput(suggestedAction);
  };

  const [messagesContainerRef, messagesEndRef] =
    useScrollToBottom<HTMLDivElement>();

  return (
    <div className="flex flex-row justify-center pb-4 md:pb-8 h-dvh bg-background">
      <div className="flex flex-col justify-between items-center gap-4">
        <div
          ref={messagesContainerRef}
          className="flex flex-col gap-4 h-full w-dvw items-center overflow-y-scroll">
          {messages.length === 0 && <Overview />}

          {messages.map((message, idx) => (
            <PreviewMessage
              key={message.id}
              chatId={idx + message.id}
              role={message.role}
              content={message.content}
            />
          ))}
          <div
            ref={messagesEndRef}
            className="shrink-0 min-w-[24px] min-h-[24px]"
          />
        </div>

        {messages.length === 0 && (
          <div className="grid sm:grid-cols-2 gap-2 w-full px-4 md:px-0 mx-auto md:max-w-[500px]">
            {suggestedActions.map((suggestedAction, index) => (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.05 * index }}
                key={index}
                className={index > 1 ? "hidden sm:block" : "block"}>
                <button
                  onClick={() => append(suggestedAction.action)}
                  className="w-full text-left border border-zinc-200 dark:border-zinc-800 text-zinc-800 dark:text-zinc-300 rounded-lg p-2 text-sm hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors flex flex-col">
                  <span className="font-medium">{suggestedAction.title}</span>
                  <span className="text-zinc-500 dark:text-zinc-400">
                    {suggestedAction.label}
                  </span>
                </button>
              </motion.div>
            ))}
          </div>
        )}

        <form className="flex flex-row gap-2 relative items-end w-full md:max-w-[500px] max-w-[calc(1000dvw-32px)] px-4 md:px-0">
          <UserInput
            input={input}
            setInput={setInput}
            handleSubmit={handleSubmit}
            isLoading={isLoading}
            stop={() => {}}
          />
        </form>
      </div>
    </div>
  );
}
