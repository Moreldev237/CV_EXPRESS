// CV Express Frontend JavaScript
// Modern ES modules, async/await, JWT auth, API utils

const API_BASE = '/api/';
const STORAGE_KEYS = {
  ACCESS_TOKEN: 'cvexpress_access_token',
  REFRESH_TOKEN: 'cvexpress_refresh_token',
  USER: 'cvexpress_user',
  THEME: 'cvexpress_theme'
};

// App initialization
async function initApp() {
  await checkAuthStatus();
  setupEventListeners();
  setupThemeToggle();
  setupMobileMenu();
}

// Check authentication status on load
async function checkAuthStatus() {
  const token = getAccessToken();
  if (token) {
    try {
      const user = await apiGet('/auth/profile/');
      updateUIForAuth(user);
      document.getElementById('user-menu')?.classList.remove('hidden');
    } catch (error) {
      clearAuth();
      updateUIForGuest();
    }
  } else {
    updateUIForGuest();
  }
}

// Update UI based on auth status
function updateUIForAuth(user) {
  const profileEl = document.getElementById('user-profile');
  const avatarEl = document.getElementById('avatar');
  const usernameEl = document.getElementById('username');
  
  if (profileEl && avatarEl && usernameEl) {
    avatarEl.src = user.profile_image || '/static/img/default-avatar.png';
    usernameEl.textContent = user.first_name || user.email.split('@')[0];
    profileEl.classList.remove('hidden');
  }
}

function updateUIForGuest() {
  const profileEl = document.getElementById('user-profile');
  if (profileEl) profileEl.classList.add('hidden');
}

// Token management
function getAccessToken() {
  return localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN);
}

function setTokens(accessToken, refreshToken, user) {
  localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, accessToken);
  localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, refreshToken);
  localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user));
}

function clearAuth() {
  localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN);
  localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN);
  localStorage.removeItem(STORAGE_KEYS.USER);
}

function logout() {
  clearAuth();
  window.location.href = '/';
}

// API Helper with auth and refresh
async function apiRequest(endpoint, options = {}) {
  const token = getAccessToken();
  const config = {
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
      ...options.headers
    },
    ...options
  };

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  try {
    const response = await fetch(API_BASE + endpoint.replace(/^\//, ''), config);
    
    if (response.status === 401) {
      const refreshToken = localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN);
      if (refreshToken) {
        const refreshResponse = await fetch(API_BASE + 'token/refresh/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ refresh: refreshToken })
        });
        
        if (refreshResponse.ok) {
          const { access } = await refreshResponse.json();
          config.headers.Authorization = `Bearer ${access}`;
          return fetch(API_BASE + endpoint.replace(/^\//, ''), config);
        }
      }
      clearAuth();
      window.location.href = '/auth/login/?next=' + window.location.pathname;
      throw new Error('Auth failed');
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.ok ? response.json() : null;
  } catch (error) {
    showToast(error.message, 'error');
    throw error;
  }
}

const apiGet = (endpoint) => apiRequest(endpoint, { method: 'GET' });
const apiPost = (endpoint, data) => apiRequest(endpoint, { 
  method: 'POST', 
  body: JSON.stringify(data || {}) 
});
const apiPut = (endpoint, data) => apiRequest(endpoint, { 
  method: 'PUT', 
  body: JSON.stringify(data || {}) 
});
const apiDelete = (endpoint) => apiRequest(endpoint, { method: 'DELETE' });

// Register user
async function registerUser(formData) {
  showLoading();
  try {
    const response = await apiPost('auth/register/', formData);
    showToast('Inscription réussie! Vérifiez votre email.', 'success');
    window.location.href = '/auth/verify-otp/';
    return response;
  } finally {
    hideLoading();
  }
}

// Verify OTP
async function verifyOTP(formData) {
  showLoading();
  try {
    const response = await apiPost('auth/verify-otp/', formData);
    localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, response.access);
    localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, response.refresh);
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(response.user));
    showToast('Compte activé! Redirection...', 'success');
    setTimeout(() => window.location.href = '/dashboard/', 1500);
  } finally {
    hideLoading();
  }
}

// Login
async function loginUser(email, password) {
  const response = await fetch(API_BASE + 'token/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  
  if (!response.ok) throw new Error('Identifiants invalides');
  
  const data = await response.json();
  setTokens(data.access, data.refresh, { email });
  window.location.href = '/dashboard/';
}

// Generic form handler
async function handleFormSubmit(event, handler) {
  event.preventDefault();
  const formData = Object.fromEntries(new FormData(event.target));
  
  try {
    await handler(formData);
  } catch (error) {
    console.error(error);
  }
}

// UI Helpers
function showToast(message, type = 'info') {
  // Create toast element
  const toast = document.createElement('div');
  toast.className = `fixed top-4 right-4 z-50 p-4 rounded-xl shadow-2xl text-white max-w-sm fade-in-up ${
    type === 'success' ? 'bg-emerald-500' : 
    type === 'error' ? 'bg-red-500' : 'bg-blue-500'
  }`;
  toast.textContent = message;
  
  document.body.appendChild(toast);
  
  setTimeout(() => {
    toast.remove();
  }, 4000);
}

function showLoading() {
  const spinner = document.createElement('div');
  spinner.id = 'global-loading';
  spinner.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
  spinner.innerHTML = '<div class="spinner bg-white p-4 rounded-full shadow-2xl"></div>';
  document.body.appendChild(spinner);
}

function hideLoading() {
  document.getElementById('global-loading')?.remove();
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Event listeners setup
function setupEventListeners() {
  // Form handlers, buttons, etc.
  document.querySelectorAll('.auth-form').forEach(form => {
    form.addEventListener('submit', async (e) => {
      // Specific handler based on form id
      const formId = form.id;
      if (formId === 'register-form') {
        e.preventDefault();
        const formData = Object.fromEntries(new FormData(form));
        await registerUser(formData);
      }
      // Add more...
    });
  });
}

function setupThemeToggle() {
  // Dark/light mode toggle
  const toggle = document.createElement('button');
  toggle.className = 'p-2 rounded-full bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 transition';
  toggle.innerHTML = '🌙';
  toggle.onclick = () => {
    document.documentElement.classList.toggle('dark');
    localStorage.theme = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
  };
  // Add to navbar...
}

function setupMobileMenu() {
  const btn = document.getElementById('mobile-menu-btn');
  const menu = document.getElementById('mobile-menu');
  if (btn) {
    btn.onclick = () => {
      menu.classList.toggle('hidden');
    };
  }
}

function toggleUserMenu() {
  document.getElementById('user-menu').classList.toggle('hidden');
}

// CV Builder specific (to be extended)
let currentCV = null;
async function loadCV(cvId) {
  currentCV = await apiGet(`cvs/${cvId}/`);
  renderCVPreview(currentCV);
}

function renderCVPreview(cv) {
  // Update preview pane
  console.log('Rendering CV:', cv);
}

// Export PDF
async function exportPDF(cvId) {
  const link = document.createElement('a');
  link.href = `/api/cvs/${cvId}/export-pdf/`;
  link.download = `cv-${cvId}.pdf`;
  link.click();
}

// Stripe integration placeholder
function initStripe() {
  // Load Stripe.js and Elements
}

// Exposed globals
window.cvApp = {
  apiGet, apiPost, apiPut, apiDelete,
  logout, checkAuthStatus,
  registerUser, verifyOTP, loginUser,
  showToast, showLoading, hideLoading,
  loadCV, exportPDF
};

console.log('CV Express Frontend loaded ✅');
