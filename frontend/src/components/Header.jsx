function Header({
    title,
    subtitle,
    darkMode,
    setDarkMode,
}) {

    return (

        <header className="app-header">

            <div className="header-content">

                <div>

                    <h1>{title}</h1>

                    <p>{subtitle}</p>

                </div>

                <button
                    className="theme-toggle"
                    onClick={() => setDarkMode(!darkMode)}
                >

                    {darkMode ? "☀️ Light" : "🌙 Dark"}

                </button>

            </div>

        </header>

    );

}

export default Header;