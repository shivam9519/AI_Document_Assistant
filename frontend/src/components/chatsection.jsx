import { useEffect, useRef } from "react";

function ChatSection({
    question,
    setQuestion,
    handleSend,
    messages,
    loading,
}) {

    const chatContainerRef = useRef(null);

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

                            <div className="message-header">

                                {message.role === "user"
                                    ? "👤 You"
                                    : "🤖 AI"}

                            </div>

                            <div className="message-body">

                                {message.text}

                            </div>

                            {message.role === "assistant" &&
                                message.sources &&
                                message.sources.length > 0 && (

                                    <div className="message-sources">

                                        <strong>Sources:</strong>{" "}

                                        {message.sources.map((page) => (

                                            <span
                                                key={page}
                                                className="source-tag"
                                            >
                                                Page {page}
                                            </span>

                                        ))}

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

                        <div className="message-body">

                            Thinking...

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