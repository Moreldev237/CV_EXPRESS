import { Link } from 'react-router-dom';
import { authService } from '../services/auth';

const Dashboard = () => {
  const handleLogout = () => {
    authService.logout();
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>CV Express - Tableau de bord</h1>
        <button onClick={handleLogout} className="logout-btn">
          Déconnexion
        </button>
      </header>

      <div className="dashboard-content">
        <div className="dashboard-grid">
          <div className="dashboard-card">
            <h3>Créer un CV</h3>
            <p>Construisez votre CV professionnel</p>
            <Link to="/cv-builder" className="btn-primary">
              Commencer
            </Link>
          </div>

          <div className="dashboard-card">
            <h3>Lettre de motivation</h3>
            <p>Générez une lettre de motivation</p>
            <Link to="/cover-letter-builder" className="btn-primary">
              Commencer
            </Link>
          </div>

          <div className="dashboard-card">
            <h3>Mon profil</h3>
            <p>Gérez vos informations personnelles</p>
            <Link to="/profile" className="btn-secondary">
              Voir le profil
            </Link>
          </div>

          <div className="dashboard-card">
            <h3>Analytics</h3>
            <p>Statistiques de vos CV</p>
            <button className="btn-secondary" disabled>
              Bientôt disponible
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;