import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

function ChatSection({
    question,
    setQuestion,
    handleSend,
    messages,
    loading,
}) {

    const chatContainerRef = useRef(null);

    const [copiedIndex, setCopiedIndex] = useState(null);

    useEffect(() => {

        if (chatContainerRef.current) {

            chatContainerRef.current.scrollTop =
                chatContainerRef.current.scrollHeight;

        }

    }, [messages, loading]);

    function handleKeyDown(event) {

        if (event.key === "Enter") {
            handleSend();
        }

    }

    async function handleCopy(text, index) {

        try {

            await navigator.clipboard.writeText(text);

            setCopiedIndex(index);

            setTimeout(() => {

                setCopiedIndex(null);

            }, 2000);

        }

        catch (error) {

            console.error(error);

        }

    }

    return (

        <section className="chat-section">

            <h2>💬 Chat</h2>

            <div
                className="chat-container"
                ref={chatContainerRef}
            >

                {messages.length === 0 ? (

                    <div className="empty-chat">

                        <p>Upload a PDF and ask your first question.</p>

                    </div>

                ) : (

                                    messages.map((message, index) => (

                                        <div
                                            key={index}
                                            className={`message ${message.role}`}
                                        >
                                            {message.role === "assistant" && (

                                            <div className="assistant-header">

                                                <div className="assistant-avatar">

                                                    🤖

                                                </div>

                                                <span>

                                                    AI Assistant

                                                </span>

                                            </div>

                                        )}

                            <div className="message-body">

                                {message.role === "assistant" ? (

                                    <ReactMarkdown
                                        remarkPlugins={[remarkGfm]}
                                    >
                                        {message.text}
                                    </ReactMarkdown>

                                ) : (

                                    message.text

                                )}

                            </div>
                            {message.role === "assistant" && (

                                <div className="message-footer">

                                    {message.sources && message.sources.length > 0 && (

                                        <div className="message-sources">

                                            <span className="sources-label">

                                                📄 Sources

                                            </span>

                                            {message.sources.map((page) => (

                                                <span
                                                    key={page}
                                                    className="source-tag"
                                                >
                                                    📄 Page {page}
                                                </span>

                                            ))}

                                        </div>

                                    )}

                                    <button
                                        className="copy-button"
                                        onClick={() => handleCopy(message.text, index)}
                                    >

                                        {copiedIndex === index
                                            ? "✅ Copied"
                                            : "📋 Copy"}

                                    </button>

                                </div>

                            )}

                       

                        </div>

                    ))

                )}

                {loading && (

                    <div className="message assistant">

                        <div className="message-header">

                            🤖 AI

                        </div>

                        <div className="message-body typing-loader">

                            <span></span>
                            <span></span>
                            <span></span>

                        </div>

                    </div>

                )}

            </div>

            <div className="chat-input">

                <input
                    type="text"
                    placeholder="Ask anything about your PDF..."
                    value={question}
                    onChange={(event) =>
                        setQuestion(event.target.value)
                    }
                    onKeyDown={handleKeyDown}
                />

                <button
                    onClick={handleSend}
                    disabled={loading}
                >
                    {loading ? "Thinking..." : "Send"}
                </button>

            </div>

        </section>

    );

}

export default ChatSection;