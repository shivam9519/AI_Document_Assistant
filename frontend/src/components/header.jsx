function Header({
    title,
    subtitle,
    onNewChat,
}) {

    return (

        <header className="app-header">

            <div className="header-content">

                <div>

                    <h1>{title}</h1>

                    <p>{subtitle}</p>

                </div>

                <button
                    className="new-chat-button"
                    onClick={onNewChat}
                >

                    ✨ New Chat

                </button>

            </div>

        </header>

    );

}

export default Header;