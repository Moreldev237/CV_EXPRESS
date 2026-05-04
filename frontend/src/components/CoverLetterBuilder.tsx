import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';

interface CoverLetter {
  id: number;
  title: string;
  template: number | null;
  template_details?: {
    id: number;
    name: string;
    description: string;
    thumbnail: string | null;
    html_path: string;
  };
  recipient_name: string;
  company_name: string;
  recipient_address: string;
  subject: string;
  content: string;
  created_at: string;
  updated_at: string;
}

interface Template {
  id: number;
  name: string;
  description: string;
  thumbnail: string | null;
  html_path: string;
}

const CoverLetterBuilder: React.FC = () => {
  const [letters, setLetters] = useState<CoverLetter[]>([]);
  const [templates, setTemplates] = useState<Template[]>([]);
  const [selectedLetter, setSelectedLetter] = useState<CoverLetter | null>(null);
  const [loading, setLoading] = useState(false);
  const [isEditing, setIsEditing] = useState(false);

  // État du formulaire
  const [formData, setFormData] = useState({
    title: '',
    template: '',
    recipient_name: '',
    company_name: '',
    recipient_address: '',
    subject: '',
    content: ''
  });

  useEffect(() => {
    loadLetters();
    loadTemplates();
  }, []);

  const loadLetters = async () => {
    try {
      const response = await api.get('/letters/');
      setLetters(response.data);
    } catch (error) {
      console.error('Erreur lors du chargement des lettres:', error);
    }
  };

  const loadTemplates = async () => {
    try {
      const response = await api.get('/templates/');
      setTemplates(response.data);
    } catch (error) {
      console.error('Erreur lors du chargement des templates:', error);
    }
  };

  const resetForm = () => {
    setFormData({
      title: '',
      template: '',
      recipient_name: '',
      company_name: '',
      recipient_address: '',
      subject: '',
      content: ''
    });
    setIsEditing(false);
    setSelectedLetter(null);
  };

  const handleCreateLetter = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const data = {
        ...formData,
        template: formData.template ? parseInt(formData.template) : null
      };
      const response = await api.post('/letters/', data);
      setLetters([...letters, response.data]);
      resetForm();
    } catch (error) {
      console.error('Erreur lors de la création de la lettre:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateLetter = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedLetter) return;
    setLoading(true);
    try {
      const data = {
        ...formData,
        template: formData.template ? parseInt(formData.template) : null
      };
      const response = await api.put(`/letters/${selectedLetter.id}/`, data);
      setLetters(letters.map(letter =>
        letter.id === selectedLetter.id ? response.data : letter
      ));
      resetForm();
    } catch (error) {
      console.error('Erreur lors de la mise à jour de la lettre:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEditLetter = (letter: CoverLetter) => {
    setSelectedLetter(letter);
    setFormData({
      title: letter.title,
      template: letter.template?.toString() || '',
      recipient_name: letter.recipient_name,
      company_name: letter.company_name,
      recipient_address: letter.recipient_address,
      subject: letter.subject,
      content: letter.content
    });
    setIsEditing(true);
  };

  const handleDeleteLetter = async (letterId: number) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cette lettre ?')) return;
    try {
      await api.delete(`/letters/${letterId}/`);
      setLetters(letters.filter(letter => letter.id !== letterId));
    } catch (error) {
      console.error('Erreur lors de la suppression de la lettre:', error);
    }
  };

  const handleExportPDF = async (letterId: number) => {
    try {
      const response = await api.get(`/letters/${letterId}/export-pdf/`, {
        responseType: 'blob'
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `lettre_${letterId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Erreur lors de l\'export PDF:', error);
    }
  };

  return (
    <div className="cover-letter-builder container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Constructeur de Lettre de Motivation</h1>
        <Link to="/dashboard" className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600">
          Retour au tableau de bord
        </Link>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Liste des lettres */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-semibold mb-6">Mes Lettres de Motivation</h2>

          {letters.length === 0 ? (
            <p className="text-gray-600">Aucune lettre de motivation créée pour le moment.</p>
          ) : (
            <div className="space-y-4">
              {letters.map(letter => (
                <div key={letter.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <h3 className="font-semibold text-lg">{letter.title}</h3>
                      <p className="text-gray-600 text-sm">
                        {letter.company_name && `Pour ${letter.company_name}`}
                        {letter.recipient_name && ` - ${letter.recipient_name}`}
                      </p>
                      <p className="text-gray-500 text-xs mt-1">
                        Créée le {new Date(letter.created_at).toLocaleDateString()}
                      </p>
                    </div>
                    <div className="flex space-x-2 ml-4">
                      <button
                        onClick={() => handleEditLetter(letter)}
                        className="bg-blue-500 text-white px-3 py-1 rounded text-sm hover:bg-blue-600"
                      >
                        Modifier
                      </button>
                      <button
                        onClick={() => handleExportPDF(letter.id)}
                        className="bg-green-500 text-white px-3 py-1 rounded text-sm hover:bg-green-600"
                      >
                        PDF
                      </button>
                      <button
                        onClick={() => handleDeleteLetter(letter.id)}
                        className="bg-red-500 text-white px-3 py-1 rounded text-sm hover:bg-red-600"
                      >
                        Suppr.
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Formulaire */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-semibold">
              {isEditing ? 'Modifier la lettre' : 'Créer une nouvelle lettre'}
            </h2>
            {isEditing && (
              <button
                onClick={resetForm}
                className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
              >
                Annuler
              </button>
            )}
          </div>

          <form onSubmit={isEditing ? handleUpdateLetter : handleCreateLetter} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Titre de la lettre</label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => setFormData({...formData, title: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Ex: Lettre pour poste de développeur"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Modèle (optionnel)</label>
              <select
                value={formData.template}
                onChange={(e) => setFormData({...formData, template: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Sélectionner un modèle</option>
                {templates.map(template => (
                  <option key={template.id} value={template.id}>{template.name}</option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Nom du destinataire</label>
                <input
                  type="text"
                  value={formData.recipient_name}
                  onChange={(e) => setFormData({...formData, recipient_name: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Ex: Madame Dupont"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Nom de l'entreprise</label>
                <input
                  type="text"
                  value={formData.company_name}
                  onChange={(e) => setFormData({...formData, company_name: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Ex: TechCorp SA"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Adresse du destinataire</label>
              <textarea
                value={formData.recipient_address}
                onChange={(e) => setFormData({...formData, recipient_address: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                rows={3}
                placeholder="Adresse complète du destinataire"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Objet de la lettre</label>
              <input
                type="text"
                value={formData.subject}
                onChange={(e) => setFormData({...formData, subject: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Ex: Candidature au poste de Développeur Full Stack"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Contenu de la lettre</label>
              <textarea
                value={formData.content}
                onChange={(e) => setFormData({...formData, content: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                rows={12}
                placeholder="Rédigez le contenu de votre lettre de motivation ici..."
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-500 text-white py-3 px-4 rounded-md hover:bg-blue-600 disabled:opacity-50 font-medium"
            >
              {loading
                ? (isEditing ? 'Mise à jour...' : 'Création...')
                : (isEditing ? 'Mettre à jour la lettre' : 'Créer la lettre')
              }
            </button>
          </form>

          {/* Aperçu rapide */}
          {formData.content && (
            <div className="mt-6 border-t pt-4">
              <h3 className="font-semibold mb-2">Aperçu rapide :</h3>
              <div className="bg-gray-50 p-4 rounded max-h-32 overflow-y-auto">
                <p className="text-sm whitespace-pre-wrap">{formData.content}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CoverLetterBuilder;