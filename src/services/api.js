import axios from 'axios';

const API_URL = 'https://info-3180-project.onrender.com/api';


const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 10000
});


apiClient.interceptors.request.use(
  config => {
 
    console.log(`Making ${config.method.toUpperCase()} request to: ${config.baseURL}${config.url}`);
    
   
    const token = localStorage.getItem('jwt');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    
    return config;
  },
  error => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

apiClient.interceptors.response.use(
  response => {
    console.log('Response received:', response.status);
    return response;
  },
  error => {
    if (error.response) {
      console.error('Server error:', error.response.status, error.response.data);
      
    
      if (error.response.status === 401) {
        localStorage.removeItem('jwt');
        localStorage.removeItem('user');
      }
    } else if (error.request) {
      console.error('Network error - no response received');
    } else {
      console.error('Error:', error.message);
    }
    
    return Promise.reject(error);
  }
);


const apiService = {
  register(userData) {
    return apiClient.post('/register', userData);
  },
  
  login(credentials) {
    console.log('Login attempt with:', credentials);
    return apiClient.post('/auth/login', credentials);
  },
  
  logout() {
    return apiClient.post('/auth/logout');
  },
  
  
  getProfiles() {
    return apiClient.get('/profiles');
  },
  
  createProfile(profileData) {
    return apiClient.post('/profiles', profileData);
  },
  
  getProfile(profileId) {
    return apiClient.get(`/profiles/${profileId}`);
  },
  
  getMatches(profileId) {
    return apiClient.get(`/profiles/matches/${profileId}`);
  },
  
  addToFavourites(userId) {
    return apiClient.post(`/profiles/${userId}/favourite`);
  },
  

  
searchProfiles(params) {
  
  const queryParams = {};
  

  if (params.name) queryParams.name = params.name;
  if (params.birth_year) queryParams.birth_year = params.birth_year;
  if (params.sex) queryParams.sex = params.sex;
  if (params.race) queryParams.race = params.race;
  if (params.parish) queryParams.parish = params.parish;
  
  console.log('Searching with params:', queryParams);
  
  return apiClient.get('/search', { params: queryParams });
},
  
  
  getUser(userId) {
    return apiClient.get(`/users/${userId}`);
  },
  
  getUserFavourites(userId, sortBy = 'name') {
    return apiClient.get(`/users/${userId}/favourites`, { 
      params: { sort_by: sortBy } 
    });
  },

  
 
 
  getProfiles(includeOwn = false) {
  console.log(`Getting profiles with includeOwn=${includeOwn}`);
  return apiClient.get('/profiles', { 
    params: { include_own: includeOwn } 
  });
},
  
  getTopFavourites(count = 20, sortBy = 'count') {
    return apiClient.get(`/users/favourites/${count}`, { 
      params: { sort_by: sortBy } 
    });
  }
};

export default apiService;