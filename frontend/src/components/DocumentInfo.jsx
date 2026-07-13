function DocumentInfo({ document }) {

    if (!document) return null;

    return (

        <section className="document-info-card">

            <div className="document-icon">

                📄

            </div>

            <div className="document-details">

                <h3>

                    {document.filename}

                </h3>

                <p>

                    🟢 Ready to chat

                </p>

                <div className="document-meta">

                    <span>

                        📑 Pages: {document.page_count ?? "--"}

                    </span>

                    <span>

                        🕒 Uploaded: Just now

                    </span>

                </div>

                <small>

                    🆔 {document.id.slice(0,12)}...

                </small>

            </div>

        </section>

    );

}

export default DocumentInfo;