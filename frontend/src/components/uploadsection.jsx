import { useState } from "react";

function UploadSection({ setDocumentId }) {

    const [file, setFile] = useState(null);
    const [uploadResult, setUploadResult] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [loading, setLoading] = useState(false);

    function handleFileChange(event) {
        const selectedFile = event.target.files[0];
        setFile(selectedFile);
    }

    async function handleUpload() {

        if (!file) {
            alert("Please select a PDF first.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        setUploading(true);

        try {

            const response = await fetch(
                "http://127.0.0.1:8000/upload",
                {
                    method: "POST",
                    body: formData,
                }
            );

            const data = await response.json();

            console.log(data);

            setUploadResult(data);

            setDocumentId(data.document_id);

        } catch (error) {

            console.error(error);

            alert("Upload Failed!");

        } finally {

            setUploading(false);

        }

    }

    return (

        <section className="upload-section">

            <h2>📄 Upload PDF</h2>

            <div className="upload-box">

                <input
                    type="file"
                    onChange={handleFileChange}
                />

                <button
                    onClick={handleUpload}
                    disabled={uploading}
                >
                    {uploading ? "Uploading..." : "Upload"}
                </button>

            </div>

            {file && (
                <p className="selected-file">

                    Selected File:
                    <strong> {file.name}</strong>

                </p>
            )}

            {uploadResult && (

                <div className="upload-success">

                    ✅ <strong>{uploadResult.filename}</strong> uploaded successfully.

                </div>

            )}

        </section>

    );
}

export default UploadSection;