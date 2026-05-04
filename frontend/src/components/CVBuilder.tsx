import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';

interface CV {
  id: number;
  title: string;
  template: number | null;
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

interface Experience {
  id: number;
  position: string;
  company: string;
  start_date: string;
  end_date: string | null;
  description: string;
  current: boolean;
}

interface Education {
  id: number;
  degree: string;
  institution: string;
  start_date: string;
  end_date: string | null;
  description: string;
  current: boolean;
}

interface Skill {
  id: number;
  name: string;
  level: string;
  category: string;
}

const CVBuilder: React.FC = () => {
  const [cvs, setCvs] = useState<CV[]>([]);
  const [templates, setTemplates] = useState<Template[]>([]);
  const [selectedCV, setSelectedCV] = useState<CV | null>(null);
  const [experiences, setExperiences] = useState<Experience[]>([]);
  const [educations, setEducations] = useState<Education[]>([]);
  const [skills, setSkills] = useState<Skill[]>([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'cvs' | 'experiences' | 'educations' | 'skills'>('cvs');

  // États pour les formulaires
  const [cvForm, setCvForm] = useState({ title: '', template: '' });
  const [experienceForm, setExperienceForm] = useState({
    position: '', company: '', start_date: '', end_date: '', description: '', current: false
  });
  const [educationForm, setEducationForm] = useState({
    degree: '', institution: '', start_date: '', end_date: '', description: '', current: false
  });
  const [skillForm, setSkillForm] = useState({ name: '', level: 'Débutant', category: '' });

  useEffect(() => {
    loadCVs();
    loadTemplates();
  }, []);

  const loadCVs = async () => {
    try {
      const response = await api.get('/cvs/');
      setCvs(response.data);
    } catch (error) {
      console.error('Erreur lors du chargement des CVs:', error);
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

  const loadCVSections = async (cvId: number) => {
    try {
      const [expRes, eduRes, skillRes] = await Promise.all([
        api.get(`/cvs/${cvId}/experiences/`),
        api.get(`/cvs/${cvId}/educations/`),
        api.get(`/cvs/${cvId}/skills/`)
      ]);
      setExperiences(expRes.data);
      setEducations(eduRes.data);
      setSkills(skillRes.data);
    } catch (error) {
      console.error('Erreur lors du chargement des sections:', error);
    }
  };

  const handleCreateCV = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await api.post('/cvs/', {
        title: cvForm.title,
        template: cvForm.template ? parseInt(cvForm.template) : null
      });
      setCvs([...cvs, response.data]);
      setCvForm({ title: '', template: '' });
    } catch (error) {
      console.error('Erreur lors de la création du CV:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectCV = (cv: CV) => {
    setSelectedCV(cv);
    loadCVSections(cv.id);
    setActiveTab('experiences');
  };

  const handleCreateExperience = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedCV) return;
    setLoading(true);
    try {
      const response = await api.post(`/cvs/${selectedCV.id}/experiences/`, experienceForm);
      setExperiences([...experiences, response.data]);
      setExperienceForm({ position: '', company: '', start_date: '', end_date: '', description: '', current: false });
    } catch (error) {
      console.error('Erreur lors de la création de l\'expérience:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateEducation = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedCV) return;
    setLoading(true);
    try {
      const response = await api.post(`/cvs/${selectedCV.id}/educations/`, educationForm);
      setEducations([...educations, response.data]);
      setEducationForm({ degree: '', institution: '', start_date: '', end_date: '', description: '', current: false });
    } catch (error) {
      console.error('Erreur lors de la création de la formation:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateSkill = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedCV) return;
    setLoading(true);
    try {
      const response = await api.post(`/cvs/${selectedCV.id}/skills/`, skillForm);
      setSkills([...skills, response.data]);
      setSkillForm({ name: '', level: 'Débutant', category: '' });
    } catch (error) {
      console.error('Erreur lors de la création de la compétence:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="cv-builder container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Constructeur de CV</h1>
        <Link to="/dashboard" className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600">
          Retour au tableau de bord
        </Link>
      </div>

      {!selectedCV ? (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-semibold mb-6">Mes CVs</h2>

          {/* Liste des CVs existants */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
            {cvs.map(cv => (
              <div key={cv.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                <h3 className="font-semibold text-lg">{cv.title}</h3>
                <p className="text-gray-600 text-sm">Créé le {new Date(cv.created_at).toLocaleDateString()}</p>
                <button
                  onClick={() => handleSelectCV(cv)}
                  className="mt-3 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 w-full"
                >
                  Modifier ce CV
                </button>
              </div>
            ))}
          </div>

          {/* Formulaire de création de CV */}
          <div className="border-t pt-6">
            <h3 className="text-xl font-semibold mb-4">Créer un nouveau CV</h3>
            <form onSubmit={handleCreateCV} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Titre du CV</label>
                <input
                  type="text"
                  value={cvForm.title}
                  onChange={(e) => setCvForm({...cvForm, title: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Modèle (optionnel)</label>
                <select
                  value={cvForm.template}
                  onChange={(e) => setCvForm({...cvForm, template: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Sélectionner un modèle</option>
                  {templates.map(template => (
                    <option key={template.id} value={template.id}>{template.name}</option>
                  ))}
                </select>
              </div>
              <button
                type="submit"
                disabled={loading}
                className="bg-green-500 text-white px-6 py-2 rounded hover:bg-green-600 disabled:opacity-50"
              >
                {loading ? 'Création...' : 'Créer le CV'}
              </button>
            </form>
          </div>
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow-md">
          {/* En-tête avec navigation */}
          <div className="border-b p-4">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-semibold">{selectedCV.title}</h2>
              <button
                onClick={() => setSelectedCV(null)}
                className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
              >
                Retour aux CVs
              </button>
            </div>

            {/* Onglets */}
            <div className="flex space-x-4 mt-4">
              {[
                { key: 'experiences', label: 'Expériences', count: experiences.length },
                { key: 'educations', label: 'Formations', count: educations.length },
                { key: 'skills', label: 'Compétences', count: skills.length }
              ].map(tab => (
                <button
                  key={tab.key}
                  onClick={() => setActiveTab(tab.key as any)}
                  className={`px-4 py-2 rounded ${
                    activeTab === tab.key
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  {tab.label} ({tab.count})
                </button>
              ))}
            </div>
          </div>

          <div className="p-6">
            {/* Contenu des onglets */}
            {activeTab === 'experiences' && (
              <div>
                <h3 className="text-xl font-semibold mb-4">Expériences professionnelles</h3>

                {/* Liste des expériences */}
                <div className="space-y-4 mb-6">
                  {experiences.map(exp => (
                    <div key={exp.id} className="border rounded p-4">
                      <h4 className="font-semibold">{exp.position} chez {exp.company}</h4>
                      <p className="text-gray-600 text-sm">
                        {new Date(exp.start_date).toLocaleDateString()} - {exp.current ? 'Présent' : exp.end_date ? new Date(exp.end_date).toLocaleDateString() : ''}
                      </p>
                      <p className="mt-2">{exp.description}</p>
                    </div>
                  ))}
                </div>

                {/* Formulaire d'ajout d'expérience */}
                <form onSubmit={handleCreateExperience} className="space-y-4 border-t pt-4">
                  <h4 className="font-semibold">Ajouter une expérience</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Poste</label>
                      <input
                        type="text"
                        value={experienceForm.position}
                        onChange={(e) => setExperienceForm({...experienceForm, position: e.target.value})}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Entreprise</label>
                      <input
                        type="text"
                        value={experienceForm.company}
                        onChange={(e) => setExperienceForm({...experienceForm, company: e.target.value})}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Date de début</label>
                      <input
                        type="date"
                        value={experienceForm.start_date}
                        onChange={(e) => setExperienceForm({...experienceForm, start_date: e.target.value})}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Date de fin</label>
                      <input
                        type="date"
                        value={experienceForm.end_date}
                        onChange={(e) => setExperienceForm({...experienceForm, end_date: e.target.value})}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        disabled={experienceForm.current}
                      />
                    </div>
                  </div>
                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      id="current-exp"
                      checked={experienceForm.current}
                      onChange={(e) => setExperienceForm({...experienceForm, current: e.target.checked, end_date: e.target.checked ? '' : experienceForm.end_date})}
                      className="mr-2"
                    />
                    <label htmlFor="current-exp" className="text-sm">Poste actuel</label>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                    <textarea
                      value={experienceForm.description}
                      onChange={(e) => setExperienceForm({...experienceForm, description: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      rows={3}
                      required
                    />
                  </div>
                  <button
                    type="submit"
                    disabled={loading}
                    className="bg-green-500 text-white px-6 py-2 rounded hover:bg-green-600 disabled:opacity-50"
                  >
                    {loading ? 'Ajout...' : 'Ajouter l\'expérience'}
                  </button>
                </form>
              </div>
            )}

            {activeTab === 'educations' && (
              <div>
                <h3 className="text-xl font-semibold mb-4">Formations</h3>

                {/* Liste des formations */}
                <div className="space-y-4 mb-6">
                  {educations.map(edu => (
                    <div key={edu.id} className="border rounded p-4">
                      <h4 className="font-semibold">{edu.degree} - {edu.institution}</h4>
                      <p className="text-gray-600 text-sm">
                        {new Date(edu.start_date).toLocaleDateString()} - {edu.current ? 'Présent' : edu.end_date ? new Date(edu.end_date).toLocaleDateString() : ''}
                      </p>
                      <p className="mt-2">{edu.description}</p>
                    </div>
                  ))}
                </div>

                {/* Formulaire d'ajout de formation */}
                <form onSubmit={handleCreateEducation} className="space-y-4 border-t pt-4">
                  <h4 className="font-semibold">Ajouter une formation</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Diplôme</label>
                      <input
                        type="text"
                        value={educationForm.degree}
                        onChange={(e) => setEducationForm({...educationForm, degree: e.target.value})}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Établissement</label>
                      <input
                        type="text"
                        value={educationForm.institution}
                        onChange={(e) => setEducationForm({...educationForm, institution: e.target.value})}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Date de début</label>
                      <input
                        type="date"
                        value={educationForm.start_date}
                        onChange={(e) => setEducationForm({...educationForm, start_date: e.target.value})}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Date de fin</label>
                      <input
                        type="date"
                        value={educationForm.end_date}
                        onChange={(e) => setEducationForm({...educationForm, end_date: e.target.value})}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        disabled={educationForm.current}
                      />
                    </div>
                  </div>
                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      id="current-edu"
                      checked={educationForm.current}
                      onChange={(e) => setEducationForm({...educationForm, current: e.target.checked, end_date: e.target.checked ? '' : educationForm.end_date})}
                      className="mr-2"
                    />
                    <label htmlFor="current-edu" className="text-sm">Formation en cours</label>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                    <textarea
                      value={educationForm.description}
                      onChange={(e) => setEducationForm({...educationForm, description: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      rows={3}
                    />
                  </div>
                  <button
                    type="submit"
                    disabled={loading}
                    className="bg-green-500 text-white px-6 py-2 rounded hover:bg-green-600 disabled:opacity-50"
                  >
                    {loading ? 'Ajout...' : 'Ajouter la formation'}
                  </button>
                </form>
              </div>
            )}

            {activeTab === 'skills' && (
              <div>
                <h3 className="text-xl font-semibold mb-4">Compétences</h3>

                {/* Liste des compétences */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
                  {skills.map(skill => (
                    <div key={skill.id} className="border rounded p-4">
                      <h4 className="font-semibold">{skill.name}</h4>
                      <p className="text-gray-600 text-sm">Niveau: {skill.level}</p>
                      {skill.category && <p className="text-gray-600 text-sm">Catégorie: {skill.category}</p>}
                    </div>
                  ))}
                </div>

                {/* Formulaire d'ajout de compétence */}
                <form onSubmit={handleCreateSkill} className="space-y-4 border-t pt-4">
                  <h4 className="font-semibold">Ajouter une compétence</h4>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Nom de la compétence</label>
                      <input
                        type="text"
                        value={skillForm.name}
                        onChange={(e) => setSkillForm({...skillForm, name: e.target.value})}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Niveau</label>
                      <select
                        value={skillForm.level}
                        onChange={(e) => setSkillForm({...skillForm, level: e.target.value})}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="Débutant">Débutant</option>
                        <option value="Intermédiaire">Intermédiaire</option>
                        <option value="Avancé">Avancé</option>
                        <option value="Expert">Expert</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Catégorie (optionnel)</label>
                      <input
                        type="text"
                        value={skillForm.category}
                        onChange={(e) => setSkillForm({...skillForm, category: e.target.value})}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Ex: Langages, Outils, Soft skills..."
                      />
                    </div>
                  </div>
                  <button
                    type="submit"
                    disabled={loading}
                    className="bg-green-500 text-white px-6 py-2 rounded hover:bg-green-600 disabled:opacity-50"
                  >
                    {loading ? 'Ajout...' : 'Ajouter la compétence'}
                  </button>
                </form>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default CVBuilder;