import { useState } from "react";
import { toast } from "react-toastify";

function UploadSection({ setDocumentId }) {

    const [file, setFile] = useState(null);
    const [uploadResult, setUploadResult] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [dragActive, setDragActive] = useState(false);

    function validateFile(selectedFile) {

        if (!selectedFile) return;

        if (selectedFile.type !== "application/pdf") {

            toast.error("Please select a PDF file.");

            return;

        }

        setFile(selectedFile);

    }

    function handleFileChange(event) {

        validateFile(event.target.files[0]);

    }

    function handleDragOver(event) {

        event.preventDefault();

        setDragActive(true);

    }

    function handleDragLeave(event) {

        event.preventDefault();

        setDragActive(false);

    }

    function handleDrop(event) {

        event.preventDefault();

        setDragActive(false);

        const droppedFile = event.dataTransfer.files[0];

        validateFile(droppedFile);

    }

    async function handleUpload() {

        if (!file) {

            toast.warning("Please select a PDF first.");

            return;

        }

        setUploading(true);

        const formData = new FormData();

        formData.append("file", file);

        try {

            const response = await fetch(
                "http://127.0.0.1:8000/upload",
                {
                    method: "POST",
                    body: formData,
                }
            );

            const data = await response.json();

            setUploadResult(data);

            setDocumentId(data.document_id);

            toast.success("PDF uploaded successfully.");

        }

        catch (error) {

            console.error(error);

            toast.error("Upload failed.");

        }

        finally {

            setUploading(false);

        }

    }

    return (

        <section className="upload-card">

            <div className="upload-icon">

                📄

            </div>

            <h2>

                Upload Your PDF

            </h2>

            <p className="upload-subtitle">

                Upload a PDF and start chatting with your document using AI.

            </p>

            <div className="upload-area">

                <label
                    htmlFor="pdf-upload"
                    className={`upload-drop-zone ${dragActive ? "drag-active" : ""}`}
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                >

                    <div className="upload-drop-icon">

                        ☁️

                    </div>

                    <h3>

                        Drag & Drop your PDF

                    </h3>

                    <p>

                        or click to browse

                  </p>
                        <input
                            id="pdf-upload"
                            type="file"
                            accept=".pdf"
                            onChange={handleFileChange}
                            hidden
                        />

                        <label
                            htmlFor="pdf-upload"
                            className="browse-button"
                        >
                            📂 Browse PDF
                        </label>

                </label>

                {file ? (

                    <div className="selected-file">

                        <div className="selected-file-name">

                            📄 {file.name}

                        </div>

                        <span>

                            Ready to upload

                        </span>

                    </div>

                ) : (

                    <div className="upload-placeholder">

                        No PDF selected

                    </div>

                )}

            </div>

            <button
                className="upload-button"
                onClick={handleUpload}
                disabled={uploading}
            >

                {uploading
                    ? "Uploading..."
                    : "Upload PDF"}

            </button>

            {uploadResult && (

               <div className="upload-success">

                    <strong>
                        ✅ {uploadResult.filename} uploaded successfully.
                    </strong>

                    <p>
                        Ready to chat.
                    </p>

                </div>

            )}

        </section>

    );

}

export default UploadSection;