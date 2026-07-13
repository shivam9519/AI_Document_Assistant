import { useState } from "react";
import { toast } from "react-toastify";
import "./App.css";

import Header from "./components/Header";
import UploadSection from "./components/UploadSection";
import ChatSection from "./components/ChatSection";
import DocumentInfo from "./components/DocumentInfo";

function App() {

    const [document, setDocument] = useState(null);

    const [question, setQuestion] = useState("");

    const [messages, setMessages] = useState([]);

    const [loading, setLoading] = useState(false);

    async function handleSend() {

        if (!question.trim()) {

            toast.warning("Please enter a question.");

            return;

        }

        if (!document) {

            toast.warning("Please upload a PDF first.");

            return;

        }

        setLoading(true);

        try {

            const response = await fetch(
                "http://127.0.0.1:8000/chat",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        document_id: document.id,
                        question: question,
                    }),
                }
            );

            const data = await response.json();

            const userMessage = {
                role: "user",
                text: question,
            };

            const aiMessage = {
                role: "assistant",
                text: data.answer,
                sources: data.sources || [],
            };

            setMessages(previous => [
                ...previous,
                userMessage,
                aiMessage,
            ]);

            setQuestion("");

        }

        catch (error) {

            console.error(error);

            toast.error("Something went wrong.");

        }

        finally {

            setLoading(false);

        }

    }

    function handleNewChat() {

        setMessages([]);

        setQuestion("");

        setLoading(false);

        toast.success("Started a new chat.");

    }

    return (

        <>

            <Header
                title="AI Document Assistant"
                subtitle="Chat with your PDF using AI"
                onNewChat={handleNewChat}
            />

            <main>

                 <UploadSection
                            setDocument={setDocument}
                        />

                        <DocumentInfo
                            document={document}
                        />

                        <ChatSection
                            question={question}
                            setQuestion={setQuestion}
                            handleSend={handleSend}
                            messages={messages}
                            loading={loading}
                />
            </main>

        </>

    );

}

export default App;