import { useState } from "react";
import "./App.css";
import { ping } from "./utils";

export type CreateChatResponseData = {
  data: {
    chat: {
      choices: Array<{
        finish_reason: string;
        index: number;
        logprobs: unknown;
        message: {
          content: string;
          refusal: unknown;
          role: string;
        };
      }>;
      content: string;
      created: number;
      id: string;
      model: string;
      object: string;
      system_fingerprint: unknown;
      usage: {
        completion_tokens: number;
        completion_tokens_details: {
          accepted_prediction_tokens: number;
          audio_tokens: number;
          reasoning_tokens: number;
          rejected_prediction_tokens: number;
        };
        prompt_tokens: number;
        prompt_tokens_details: {
          audio_tokens: number;
          cached_tokens: number;
        };
        total_tokens: number;
      };
    };
  };
  message: string;
  reason: unknown;
};

const FLASK_URL = "http://localhost:8080/api";

function App() {
  const [content, setContent] = useState("");
  const [role, setRole] = useState("");
  const [responseValue, setResponseValue] = useState("");
  const [isLoading, setLoading] = useState(false);

  const onSubmit = async (): Promise<void> => {
    if (content.length < 1) {
      alert("Please specify content");
    }

    setLoading(true);
    setResponseValue("");

    const jsonData = {
      role: role,
      content: content,
    };

    // Send the JSON to the server
    const response = await fetch(`${FLASK_URL}/chats/new`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(jsonData),
    });

    setLoading(false);
    if (!response.ok) {
      setResponseValue("No chat :(");
      return;
    }
    const responseData: CreateChatResponseData = await response.json();

    const text =
      responseData.data.chat.content ||
      "Response received but no message found.";

    simulateTypingEffect(text);
  };

  function simulateTypingEffect(text: string) {
    let index = -1;
    console.log("text:", text);

    const interval = setInterval(() => {
      setResponseValue((prev) => {
        console.log("prev is", prev);
        return prev + text[index];
      });
      index++;
      if (index === text.length - 1) {
        clearInterval(interval);
      }
    }, 50);
  }

  return (
    <>
      <div className="container">
        <h1>Submit JSON</h1>
        <form id="jsonForm">
          <label htmlFor="content">Content:</label>
          <input type="text" onChange={(e) => setContent(e.target.value)} />

          <label htmlFor="role">Role:</label>
          <input type="text" onChange={(e) => setRole(e.target.value)} />

          <button type="button" onClick={() => ping()}>
            Ping
          </button>
          <button type="button" onClick={() => onSubmit()}>
            {isLoading ? "Loading..." : "Submit"}
          </button>
        </form>
        <div id="responseBox" className="response-box">
          {responseValue}
        </div>
      </div>
    </>
  );
}

export default App;
