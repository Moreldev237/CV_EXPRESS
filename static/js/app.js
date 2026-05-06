/**
 * ═══════════════════════════════════════════════════════════════
 * CV_EXPRESS - Application Frontend Complète
 * ═══════════════════════════════════════════════════════════════
 * 
 * Gère:
 * - Authentication (JWT)
 * - Navigation frontend
 * - Communication avec l'API backend
 * - État utilisateur et CV
 * - Validation et feedback
 */

const API_BASE_URL = '/api';

// ═══════════════════════════════════════════════════════════════
// 🎯 ÉTAT GLOBAL DE L'APPLICATION
// ═══════════════════════════════════════════════════════════════
const appState = {
    user: null,
    currentCV: null,
    cvList: [],
    isAuthenticated: false,
    isLoading: false,
    notifications: []
};

// ═══════════════════════════════════════════════════════════════
// 🔐 GESTION DES TOKENS & AUTHENTIFICATION
// ═══════════════════════════════════════════════════════════════
const AuthService = {
    setTokens(access, refresh) {
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
        appState.isAuthenticated = true;
    },

    getAccessToken() {
        return localStorage.getItem('access_token');
    },

    getRefreshToken() {
        return localStorage.getItem('refresh_token');
    },

    clearTokens() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        appState.isAuthenticated = false;
        appState.user = null;
        appState.currentCV = null;
    },

    async refreshToken() {
        try {
            const refresh = this.getRefreshToken();
            if (!refresh) throw new Error('No refresh token');

            const response = await fetch(`${API_BASE_URL}/auth/refresh/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh })
            });

            if (!response.ok) {
                this.clearTokens();
                window.location.href = '/auth/login/';
                return false;
            }

            const data = await response.json();
            localStorage.setItem('access_token', data.access);
            return true;
        } catch (error) {
            console.error('Token refresh failed:', error);
            this.clearTokens();
            window.location.href = '/auth/login/';
            return false;
        }
    },

    async login(email, password) {
        try {
            showNotification('Connexion...', 'info', false);
            const response = await APIRequest('/auth/login/', 'POST', { 
                username: email, 
                password 
            });
            
            this.setTokens(response.access, response.refresh);
            await UserService.fetchCurrentUser();
            showNotification('Connecté avec succès!', 'success');
            window.location.href = '/dashboard/';
            return true;
        } catch (error) {
            showNotification(error.detail || 'Erreur de connexion', 'error');
            return false;
        }
    },

    async register(userData) {
        try {
            showNotification('Inscription en cours...', 'info', false);
            const response = await APIRequest('/register/', 'POST', userData);
            showNotification('Inscription réussie! Vérifiez votre email.', 'success');
            return response;
        } catch (error) {
            showNotification(error.detail || 'Erreur lors de l\'inscription', 'error');
            return null;
        }
    },

    async verifyOTP(email, code) {
        try {
            showNotification('Vérification du code...', 'info', false);
            const response = await APIRequest('/auth/verify-otp/', 'POST', { 
                email, 
                code 
            });
            
            this.setTokens(response.access, response.refresh);
            showNotification('Email vérifié avec succès!', 'success');
            window.location.href = '/dashboard/';
            return true;
        } catch (error) {
            showNotification(error.detail || 'Code invalide', 'error');
            return false;
        }
    },

    async resendOTP(email) {
        try {
            await APIRequest('/auth/resend-otp/', 'POST', { email });
            showNotification('Code renvoyé par email', 'success');
            return true;
        } catch (error) {
            showNotification('Erreur lors de l\'envoi du code', 'error');
            return false;
        }
    },

    logout() {
        this.clearTokens();
        window.location.href = '/';
    }
};

// ═══════════════════════════════════════════════════════════════
// 👤 GESTION DES UTILISATEURS
// ═══════════════════════════════════════════════════════════════
const UserService = {
    async fetchCurrentUser() {
        try {
            const user = await APIRequest('/profile/', 'GET');
            appState.user = user;
            updateUIWithUser(user);
            return user;
        } catch (error) {
            console.error('Failed to fetch user:', error);
            return null;
        }
    },

    async updateProfile(data) {
        try {
            showNotification('Mise à jour...', 'info', false);
            const updated = await APIRequest('/profile/update/', 'PUT', data);
            appState.user = updated;
            showNotification('Profil mis à jour!', 'success');
            return updated;
        } catch (error) {
            showNotification('Erreur lors de la mise à jour', 'error');
            return null;
        }
    },

    async uploadProfileImage(file) {
        try {
            showNotification('Téléchargement...', 'info', false);
            const formData = new FormData();
            formData.append('profile_image', file);
            
            const updated = await APIRequest('/profile/upload-image/', 'POST', formData, true);
            appState.user = updated;
            updateUIWithUser(updated);
            showNotification('Photo mise à jour!', 'success');
            return updated;
        } catch (error) {
            showNotification('Erreur lors du téléchargement', 'error');
            return null;
        }
    }
};

// ═══════════════════════════════════════════════════════════════
// 📄 GESTION DES CV
// ═══════════════════════════════════════════════════════════════
const CVService = {
    async listCVs() {
        try {
            const cvs = await APIRequest('/cvs/', 'GET');
            appState.cvList = cvs;
            return cvs;
        } catch (error) {
            console.error('Failed to fetch CVs:', error);
            return [];
        }
    },

    async getCV(cvId) {
        try {
            const cv = await APIRequest(`/cvs/${cvId}/`, 'GET');
            appState.currentCV = cv;
            return cv;
        } catch (error) {
            console.error('Failed to fetch CV:', error);
            return null;
        }
    },

    async getFullCV(cvId) {
        try {
            const cv = await APIRequest(`/cvs/${cvId}/full/`, 'GET');
            appState.currentCV = cv;
            return cv;
        } catch (error) {
            console.error('Failed to fetch full CV:', error);
            return null;
        }
    },

    async createCV(title, templateId = null) {
        try {
            showNotification('Création du CV...', 'info', false);
            const cv = await APIRequest('/cvs/', 'POST', {
                title,
                template: templateId
            });
            appState.cvList.push(cv);
            showNotification('CV créé avec succès!', 'success');
            return cv;
        } catch (error) {
            showNotification('Erreur lors de la création', 'error');
            return null;
        }
    },

    async updateCV(cvId, data) {
        try {
            showNotification('Mise à jour...', 'info', false);
            const cv = await APIRequest(`/cvs/${cvId}/`, 'PUT', data);
            appState.currentCV = cv;
            showNotification('CV mis à jour!', 'success');
            return cv;
        } catch (error) {
            showNotification('Erreur lors de la mise à jour', 'error');
            return null;
        }
    },

    async deleteCV(cvId) {
        try {
            if (!confirm('Êtes-vous sûr?')) return false;
            showNotification('Suppression...', 'info', false);
            await APIRequest(`/cvs/${cvId}/`, 'DELETE');
            appState.cvList = appState.cvList.filter(cv => cv.id !== cvId);
            showNotification('CV supprimé!', 'success');
            return true;
        } catch (error) {
            showNotification('Erreur lors de la suppression', 'error');
            return false;
        }
    },

    async exportPDF(cvId) {
        try {
            showNotification('Génération du PDF...', 'info', false);
            const response = await fetch(`${API_BASE_URL}/cvs/${cvId}/export-pdf/`, {
                method: 'GET',
                headers: { 'Authorization': `Bearer ${AuthService.getAccessToken()}` }
            });
            
            if (!response.ok) throw new Error('Export failed');
            
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `CV_${appState.currentCV.title}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            showNotification('PDF téléchargé!', 'success');
            return true;
        } catch (error) {
            showNotification('Erreur lors de l\'export', 'error');
            return false;
        }
    }
};

// ═══════════════════════════════════════════════════════════════
// 💼 GESTION DES SECTIONS DU CV
// ═══════════════════════════════════════════════════════════════
const CVSectionService = {
    // Expériences
    async addExperience(cvId, data) {
        try {
            const exp = await APIRequest(`/cvs/${cvId}/experiences/`, 'POST', data);
            if (appState.currentCV) appState.currentCV.experiences.push(exp);
            showNotification('Expérience ajoutée!', 'success');
            return exp;
        } catch (error) {
            showNotification('Erreur lors de l\'ajout', 'error');
            return null;
        }
    },

    async updateExperience(expId, data) {
        try {
            const exp = await APIRequest(`/experiences/${expId}/`, 'PUT', data);
            showNotification('Expérience mise à jour!', 'success');
            return exp;
        } catch (error) {
            showNotification('Erreur lors de la mise à jour', 'error');
            return null;
        }
    },

    async deleteExperience(expId) {
        try {
            await APIRequest(`/experiences/${expId}/`, 'DELETE');
            showNotification('Expérience supprimée!', 'success');
            return true;
        } catch (error) {
            showNotification('Erreur lors de la suppression', 'error');
            return false;
        }
    },

    // Formations
    async addEducation(cvId, data) {
        try {
            const edu = await APIRequest(`/cvs/${cvId}/educations/`, 'POST', data);
            if (appState.currentCV) appState.currentCV.educations.push(edu);
            showNotification('Formation ajoutée!', 'success');
            return edu;
        } catch (error) {
            showNotification('Erreur lors de l\'ajout', 'error');
            return null;
        }
    },

    async updateEducation(eduId, data) {
        try {
            const edu = await APIRequest(`/educations/${eduId}/`, 'PUT', data);
            showNotification('Formation mise à jour!', 'success');
            return edu;
        } catch (error) {
            showNotification('Erreur lors de la mise à jour', 'error');
            return null;
        }
    },

    async deleteEducation(eduId) {
        try {
            await APIRequest(`/educations/${eduId}/`, 'DELETE');
            showNotification('Formation supprimée!', 'success');
            return true;
        } catch (error) {
            showNotification('Erreur lors de la suppression', 'error');
            return false;
        }
    },

    // Compétences
    async addSkill(cvId, data) {
        try {
            const skill = await APIRequest(`/cvs/${cvId}/skills/`, 'POST', data);
            if (appState.currentCV) appState.currentCV.skills.push(skill);
            showNotification('Compétence ajoutée!', 'success');
            return skill;
        } catch (error) {
            showNotification('Erreur lors de l\'ajout', 'error');
            return null;
        }
    },

    async updateSkill(skillId, data) {
        try {
            const skill = await APIRequest(`/skills/${skillId}/`, 'PUT', data);
            showNotification('Compétence mise à jour!', 'success');
            return skill;
        } catch (error) {
            showNotification('Erreur lors de la mise à jour', 'error');
            return null;
        }
    },

    async deleteSkill(skillId) {
        try {
            await APIRequest(`/skills/${skillId}/`, 'DELETE');
            showNotification('Compétence supprimée!', 'success');
            return true;
        } catch (error) {
            showNotification('Erreur lors de la suppression', 'error');
            return false;
        }
    },

    // Langues
    async addLanguage(cvId, data) {
        try {
            const lang = await APIRequest(`/cvs/${cvId}/languages/`, 'POST', data);
            if (appState.currentCV) appState.currentCV.languages.push(lang);
            showNotification('Langue ajoutée!', 'success');
            return lang;
        } catch (error) {
            showNotification('Erreur lors de l\'ajout', 'error');
            return null;
        }
    },

    async updateLanguage(langId, data) {
        try {
            const lang = await APIRequest(`/languages/${langId}/`, 'PUT', data);
            showNotification('Langue mise à jour!', 'success');
            return lang;
        } catch (error) {
            showNotification('Erreur lors de la mise à jour', 'error');
            return null;
        }
    },

    async deleteLanguage(langId) {
        try {
            await APIRequest(`/languages/${langId}/`, 'DELETE');
            showNotification('Langue supprimée!', 'success');
            return true;
        } catch (error) {
            showNotification('Erreur lors de la suppression', 'error');
            return false;
        }
    },

    // Projets
    async addProject(cvId, data) {
        try {
            const proj = await APIRequest(`/cvs/${cvId}/projects/`, 'POST', data);
            if (appState.currentCV) appState.currentCV.projects.push(proj);
            showNotification('Projet ajouté!', 'success');
            return proj;
        } catch (error) {
            showNotification('Erreur lors de l\'ajout', 'error');
            return null;
        }
    },

    async updateProject(projId, data) {
        try {
            const proj = await APIRequest(`/projects/${projId}/`, 'PUT', data);
            showNotification('Projet mis à jour!', 'success');
            return proj;
        } catch (error) {
            showNotification('Erreur lors de la mise à jour', 'error');
            return null;
        }
    },

    async deleteProject(projId) {
        try {
            await APIRequest(`/projects/${projId}/`, 'DELETE');
            showNotification('Projet supprimé!', 'success');
            return true;
        } catch (error) {
            showNotification('Erreur lors de la suppression', 'error');
            return false;
        }
    }
};

// ═══════════════════════════════════════════════════════════════
// 📋 GESTION DES ABONNEMENTS
// ═══════════════════════════════════════════════════════════════
const SubscriptionService = {
    async getSubscriptionStatus() {
        try {
            return await APIRequest('/subscriptions/status/', 'GET');
        } catch (error) {
            console.error('Failed to fetch subscription:', error);
            return null;
        }
    },

    async listPlans() {
        try {
            return await APIRequest('/subscriptions/plans/', 'GET');
        } catch (error) {
            console.error('Failed to fetch plans:', error);
            return [];
        }
    },

    async subscribe(planId) {
        try {
            showNotification('Souscription en cours...', 'info', false);
            const sub = await APIRequest('/subscriptions/subscribe/', 'POST', { plan_id: planId });
            showNotification('Souscription réussie!', 'success');
            return sub;
        } catch (error) {
            showNotification('Erreur lors de la souscription', 'error');
            return null;
        }
    },

    async cancel() {
        try {
            if (!confirm('Êtes-vous sûr?')) return false;
            showNotification('Annulation...', 'info', false);
            await APIRequest('/subscriptions/cancel/', 'POST', {});
            showNotification('Abonnement annulé', 'success');
            return true;
        } catch (error) {
            showNotification('Erreur lors de l\'annulation', 'error');
            return false;
        }
    }
};

// ═══════════════════════════════════════════════════════════════
// 📊 GESTION DES NOTIFICATIONS
// ═══════════════════════════════════════════════════════════════
const NotificationService = {
    async getNotifications() {
        try {
            return await APIRequest('/notifications/', 'GET');
        } catch (error) {
            console.error('Failed to fetch notifications:', error);
            return [];
        }
    },

    async markAsRead(notificationId) {
        try {
            return await APIRequest(`/notifications/${notificationId}/mark-as-read/`, 'POST', {});
        } catch (error) {
            console.error('Failed to mark notification as read:', error);
            return null;
        }
    }
};

// ═══════════════════════════════════════════════════════════════
// 🌐 REQUÊTES API GÉNÉRIQUE
// ═══════════════════════════════════════════════════════════════
async function APIRequest(endpoint, method = 'GET', data = null, isMultipart = false) {
    const url = endpoint.startsWith('http') ? endpoint : `${API_BASE_URL}${endpoint}`;
    
    const headers = {};
    const token = AuthService.getAccessToken();
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    let body = data;
    if (data && !isMultipart) {
        headers['Content-Type'] = 'application/json';
        body = JSON.stringify(data);
    }

    try {
        const response = await fetch(url, { method, headers, body });
        
        // Gestion 401 - Refresher le token
        if (response.status === 401) {
            const refreshed = await AuthService.refreshToken();
            if (refreshed) return APIRequest(endpoint, method, data, isMultipart);
            throw new Error('Unauthorized');
        }

        // Pas de contenu
        if (response.status === 204) return null;
        
        const result = await response.json();
        if (!response.ok) throw result;
        return result;
    } catch (error) {
        console.error(`API Error (${endpoint}):`, error);
        throw error;
    }
}

// ═══════════════════════════════════════════════════════════════
// 🎨 INTERFACE UTILISATEUR
// ═══════════════════════════════════════════════════════════════

// Mise à jour UI avec les infos utilisateur
function updateUIWithUser(user) {
    const userProfile = document.getElementById('user-profile');
    const username = document.getElementById('dashboard-username');
    
    if (userProfile) {
        const img = userProfile.querySelector('img');
        if (img) img.src = user.profile_image?.url || '/static/img/default-avatar.png';
        const span = userProfile.querySelector('span');
        if (span) span.textContent = user.first_name || user.email.split('@')[0];
    }
    
    if (username) {
        username.textContent = user.first_name || user.email.split('@')[0];
    }
}

// Afficher notification
function showNotification(message, type = 'info', autoClose = true) {
    const notification = document.createElement('div');
    const bgColor = {
        'success': 'bg-green-500',
        'error': 'bg-red-500',
        'info': 'bg-blue-500',
        'warning': 'bg-yellow-500'
    }[type] || 'bg-blue-500';

    notification.className = `${bgColor} text-white px-6 py-3 rounded-lg shadow-lg fixed top-4 right-4 z-50 animate-fade-in`;
    notification.textContent = message;
    document.body.appendChild(notification);

    if (autoClose) {
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    return notification;
}

// Menu utilisateur
function toggleUserMenu() {
    const menu = document.getElementById('user-menu');
    if (menu) menu.classList.toggle('hidden');
}

// Logout
function logout() {
    AuthService.logout();
}

// ═══════════════════════════════════════════════════════════════
// 🚀 INITIALISATION
// ═══════════════════════════════════════════════════════════════

// Vérifier l'authentification au chargement
document.addEventListener('DOMContentLoaded', async () => {
    const token = AuthService.getAccessToken();
    
    if (token) {
        appState.isAuthenticated = true;
        try {
            await UserService.fetchCurrentUser();
        } catch (error) {
            console.warn('Failed to fetch user on init:', error);
        }
    }
});

// Alias globaux pour compatibilité avec HTML
const cvApp = {
    login: (email, password) => AuthService.login(email, password),
    register: (data) => AuthService.register(data),
    logout: () => AuthService.logout(),
    getCurrentUser: () => UserService.fetchCurrentUser(),
    saveCV: (cvId, cvData) => CVService.updateCV(cvId, cvData),
    createCV: (title) => CVService.createCV(title),
    deleteCV: (cvId) => CVService.deleteCV(cvId),
    exportPDF: (cvId) => CVService.exportPDF(cvId),
};