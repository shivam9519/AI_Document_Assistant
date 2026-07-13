function Header({
    title,
    subtitle,
}) {

    return (

        <header className="app-header">


                <div>

                    <h1>{title}</h1>

                    <p>{subtitle}</p>

                </div>

               

          

        </header>

    );

}

export default Header;