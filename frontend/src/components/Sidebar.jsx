function Sidebar({
    handleNewChat,
    documents,
    setDocument,
    selectedDocument,
    handleDeleteDocument,
    searchTerm,
    setSearchTerm,
})  {
    const filteredDocuments = documents.filter((doc) =>
    doc.filename
        .toLowerCase()
        .includes(searchTerm.toLowerCase())
);

    return (

        <aside className="sidebar">

            <button
                className="sidebar-new-chat"
                onClick={handleNewChat}
            >
                ✨ New Chat
            </button>
            <input
    type="text"
    className="sidebar-search"
    placeholder="🔍 Search documents..."
    value={searchTerm}
    onChange={(event) =>
        setSearchTerm(event.target.value)
    }
/>

            <div className="sidebar-divider"></div>

            <div className="sidebar-title">
                Documents
            </div>

            {documents.length === 0 ? (

    <div className="sidebar-empty">
        No documents yet
    </div>

) : filteredDocuments.length === 0 ? (

    <div className="sidebar-empty">
        No matching documents found
    </div>

) : (

    filteredDocuments.map((doc) => (

        <div
            key={doc.id}
            className={
                selectedDocument?.id === doc.id
                    ? "document-item active"
                    : "document-item"
            }
            onClick={() => setDocument(doc)}
        >

            <div className="document-content">

                <div>📄</div>

                <div>

                    <strong>{doc.filename}</strong>

                    <p>
                        {doc.totalChunks ?? "--"} chunks
                    </p>

                </div>

            </div>

            <button
                className="delete-document-button"
                onClick={(event) => {

                    event.stopPropagation();

                    handleDeleteDocument(doc.id);

                }}
            >
                🗑️
            </button>

        </div>

    ))

)}
        </aside>

    );

}

export default Sidebar;