import { useState } from "react";

function Counter() {

    const [count, setCount] = useState(0);

    return (
        <>
            <h2>Count: {count}</h2>

            <button onClick={() => setCount(count + 1)}>
                Increase
            </button>
        </>
    );
}

export default Counter;