import { useState } from "react";

function FileUpload() {

    const [file, setFile] = useState(null);

    function handleFileChange(event) {
        const selectedFile = event.target.files[0];

        setFile(selectedFile);
    }

    return (
        <>
            <input
                type="file"
                onChange={handleFileChange}
            />

            <h3>
                Selected File:
                {file ? file.name : " No file selected"}
            </h3>
        </>
    );
}

export default FileUpload;