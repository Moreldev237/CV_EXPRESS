import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="home">
      <header className="home-header">
        <h1>CV Express</h1>
        <p>Créez des CV professionnels et des lettres de motivation avec l'aide de l'IA</p>
        <div className="home-actions">
          <Link to="/register" className="btn-primary">
            S'inscrire
          </Link>
          <Link to="/login" className="btn-secondary">
            Se connecter
          </Link>
        </div>
      </header>

      <section className="features">
        <div className="feature">
          <h3>CV Professionnel</h3>
          <p>Créez des CV modernes et attrayants</p>
        </div>
        <div className="feature">
          <h3>Lettres de Motivation</h3>
          <p>Générez des lettres personnalisées</p>
        </div>
        <div className="feature">
          <h3>IA Assistée</h3>
          <p>Bénéficiez de suggestions intelligentes</p>
        </div>
      </section>
    </div>
  );
};

export default Home;