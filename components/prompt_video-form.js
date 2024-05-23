import { useEffect, useState } from "react";
import Message from "./message";
import React from 'react';


export default function PromptVideoForm({
  src,
  initialPrompt,
  isFirstPrompt,
  onSubmit,
  disabled = false,
}) {
  const [prompt, setPrompt] = useState(initialPrompt);

  useEffect(() => {
    setPrompt(initialPrompt);
  }, [initialPrompt]);


  const handleSubmit = (e) => {
    e.preventDefault();
    setPrompt("");
    onSubmit(e);
  };
  

  if (disabled) {
    return;
  }

  
  return (
    <form onSubmit={handleSubmit} className="animate-in fade-in duration-700">
      <Message sender="replicate" isSameSender>
        <label htmlFor="prompt-input">
          {isFirstPrompt
            ? "What should we draw?"
            : "What should we draw now?"}
        </label>
      </Message>

    <div>
    <video controls  preload="none" aria-label="Video player" hight='50' width="700">
        <source src={src} type="video/mp4" />
        <source src={src} type="video/webm" />
        Your browser does not support the video tag.
      </video>
    </div>

      <div className="flex mt-8">
        <input
          id="prompt-input"
          type="text"
          name="prompt"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Your message..."
          className={`block w-full flex-grow${
            disabled ? "rounded-md" : "rounded-l-md"
          }`}
          disabled={disabled}
        />

        {disabled || (
          <button
            className="bg-black text-white rounded-r-md text-small inline-block p-3 flex-none"
            type="submit"
          >
            Paint
          </button>
        )}
      </div>
    </form>
  );
}
