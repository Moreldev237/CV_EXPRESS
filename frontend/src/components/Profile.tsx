import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../services/api';
import { authService } from '../services/auth';
import type { User } from '../services/auth';

const Profile = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const loadProfile = async () => {
      if (!authService.isAuthenticated()) {
        navigate('/login');
        return;
      }

      try {
        const response = await api.get('/profile/');
        setUser(response.data);
      } catch (err: any) {
        setError('Impossible de récupérer le profil.');
      } finally {
        setLoading(false);
      }
    };

    loadProfile();
  }, [navigate]);

  if (loading) {
    return (
      <div className="profile-page">
        <h2>Mon Profil</h2>
        <p>Chargement...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="profile-page">
        <h2>Mon Profil</h2>
        <p className="error-message">{error}</p>
        <Link to="/dashboard" className="btn-secondary">
          Retour au tableau de bord
        </Link>
      </div>
    );
  }

  return (
    <div className="profile-page">
      <header className="profile-header">
        <h2>Mon Profil</h2>
        <Link to="/dashboard" className="btn-secondary">
          Retour au tableau de bord
        </Link>
      </header>
      <div className="profile-card">
        <p>
          <strong>Prénom :</strong> {user?.first_name || '-'}
        </p>
        <p>
          <strong>Nom :</strong> {user?.last_name || '-'}
        </p>
        <p>
          <strong>Email :</strong> {user?.email || '-'}
        </p>
      </div>
    </div>
  );
};

export default Profile;
