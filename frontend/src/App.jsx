import { useState, useEffect } from "react";

import { toast } from "react-toastify";
import "./App.css";

import Header from "./components/Header";
import UploadSection from "./components/UploadSection";
import ChatSection from "./components/ChatSection";
import DocumentInfo from "./components/DocumentInfo";
import Sidebar from "./components/Sidebar";
function App() {

    const [document, setDocument] = useState(null);

    const [question, setQuestion] = useState("");

    const [messages, setMessages] = useState([]);
    const [currentChatId, setCurrentChatId] = useState(null);

    const [loading, setLoading] = useState(false);
    const [searchTerm, setSearchTerm] = useState("");
    const [documents, setDocuments] = useState(() => {

    const saved = localStorage.getItem("documents");

    return saved ? JSON.parse(saved) : [];

});
    const [chatHistory, setChatHistory] = useState({});
        useEffect(() => {

    localStorage.setItem(
        "documents",
        JSON.stringify(documents)
    );

}, [documents]);
   

    async function handleSend() {
        console.log(document);

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

                 setMessages((previousMessages) => {

    const updatedMessages = [
        ...previousMessages,
        userMessage,
        aiMessage,
    ];

    setChatHistory((previousHistory) => ({
        ...previousHistory,
        [document.id]: updatedMessages,
    }));

    return updatedMessages;

});

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

    if (!document) {
        toast.warning("Select a document first.");
        return;
    }

    const newChatId = Date.now().toString();

    setCurrentChatId(newChatId);

    setMessages([]);

    setQuestion("");

    setLoading(false);

    setChatHistory((previous) => ({

        ...previous,

        [document.id]: [

            ...(previous[document.id] || []),

            {
                id: newChatId,
                messages: [],
            },

        ],

    }));

    toast.success("New chat created.");

}
   function handleSelectDocument(doc) {

    console.log("Selected:", doc.id);

    console.log("History:", chatHistory);

    setDocument(doc);

    setMessages(chatHistory[doc.id] || []);

}

function handleDeleteDocument(documentId) {

    const updatedDocuments = documents.filter(
        (doc) => doc.id !== documentId
    );

    setDocuments(updatedDocuments);

    setChatHistory((previous) => {

        const updatedHistory = { ...previous };

        delete updatedHistory[documentId];

        return updatedHistory;

    });

    if (document?.id === documentId) {

        if (updatedDocuments.length > 0) {

            handleSelectDocument(updatedDocuments[0]);

        } else {

            setDocument(null);

            setMessages([]);

        }

    }

    toast.success("Document deleted.");

}
    console.log(document);

   return (

    <div className="app-layout">
<Sidebar
    handleNewChat={handleNewChat}
    documents={documents}
    setDocument={handleSelectDocument}
    selectedDocument={document}
    handleDeleteDocument={handleDeleteDocument}
    searchTerm={searchTerm}
    setSearchTerm={setSearchTerm}
/>

        <div className="app-content">

            <Header
                title="AI Document Assistant"
                subtitle="Chat with your PDF using AI"
            />

            <main>

                <UploadSection
                        setDocument={setDocument}
                        setDocuments={setDocuments}
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

        </div>

    </div>

);

}

export default App;