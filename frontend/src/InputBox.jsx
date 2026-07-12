import { useState } from "react";

function InputBox() {

    const [name, setName] = useState("");

    return (
        <>
            <input
                type="text"
                placeholder="Enter your name"
                value={name}
                onChange={(event) => setName(event.target.value)}
            />

            <h2>Hello {name}</h2>
        </>
    );
}

export default InputBox;