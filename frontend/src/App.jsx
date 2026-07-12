import { useState } from "react";

import Header from "./components/Header";
import UploadSection from "./components/UploadSection";
import ChatSection from "./components/ChatSection";

function App() {

    const [documentId, setDocumentId] = useState(null);

    const [question, setQuestion] = useState("");

    const [messages, setMessages] = useState([]);

    const [loading, setLoading] = useState(false);

    async function handleSend() {

        if (!question.trim()) {
            return;
        }

        if (!documentId) {
            alert("Please upload a PDF first.");
            return;
        }

        const userQuestion = question;

        setQuestion("");

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
                        document_id: documentId,
                        question: userQuestion,
                    }),
                }
            );

            const data = await response.json();

            console.log(data);

            setMessages((previousMessages) => [

                ...previousMessages,

                {
                    role: "user",
                    text: userQuestion,
                },

                {
                    role: "assistant",
                    text: data.answer,
                    sources: data.sources,
                },

            ]);

        }

        catch (error) {

            console.error(error);

            alert("Something went wrong.");

        }

        finally {

            setLoading(false);

        }

    }

    return (

        <>

            <Header
                title="AI Document Assistant"
                subtitle="Chat with your PDF using AI"
            />

            <main>

                <UploadSection
                    setDocumentId={setDocumentId}
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