<template>
  <div class="new-profile">
    <h2 class="mb-4">Create New Profile</h2>
    
    <div class="card">
      <div class="card-body">
        <form @submit.prevent="createProfile">
          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="description" class="form-label">Short Description:</label>
              <input 
                type="text" 
                id="description" 
                v-model="profile.description" 
                class="form-control" 
                required
              />
            </div>
            
            <div class="col-md-6 mb-3">
              <label for="parish" class="form-label">Parish:</label>
              <select 
                id="parish" 
                v-model="profile.parish" 
                class="form-select" 
                required
              >
                <option value="">Select Parish</option>
                <option value="Kingston">Kingston</option>
                <option value="St. Andrew">St. Andrew</option>
                <option value="St. Catherine">St. Catherine</option>
                <option value="Clarendon">Clarendon</option>
                <option value="Manchester">Manchester</option>
                <option value="St. Elizabeth">St. Elizabeth</option>
                <option value="Westmoreland">Westmoreland</option>
                <option value="Hanover">Hanover</option>
                <option value="St. James">St. James</option>
                <option value="Trelawny">Trelawny</option>
                <option value="St. Ann">St. Ann</option>
                <option value="St. Mary">St. Mary</option>
                <option value="Portland">Portland</option>
                <option value="St. Thomas">St. Thomas</option>
              </select>
            </div>
            
            <div class="col-md-12 mb-3">
              <label for="biography" class="form-label">Biography:</label>
              <textarea 
                id="biography" 
                v-model="profile.biography" 
                class="form-control" 
                rows="4" 
                required
              ></textarea>
            </div>
            
            <div class="col-md-6 mb-3">
              <label for="sex" class="form-label">Sex:</label>
              <select 
                id="sex" 
                v-model="profile.sex" 
                class="form-select" 
                required
              >
                <option value="">Select Sex</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>
            
            <div class="col-md-6 mb-3">
              <label for="race" class="form-label">Race:</label>
              <input 
                type="text" 
                id="race" 
                v-model="profile.race" 
                class="form-control" 
                required
              />
            </div>
            
            <div class="col-md-6 mb-3">
              <label for="birthYear" class="form-label">Birth Year:</label>
              <input 
                type="number" 
                id="birthYear" 
                v-model="profile.birth_year" 
                class="form-control" 
                min="1900" 
                :max="currentYear" 
                required
              />
            </div>
            
            <div class="col-md-6 mb-3">
              <label for="height" class="form-label">Height (inches):</label>
              <input 
                type="number" 
                id="height" 
                v-model="profile.height" 
                class="form-control" 
                step="0.1" 
                min="36" 
                max="96" 
                required
              />
            </div>
            
            <div class="col-md-6 mb-3">
              <label for="favCuisine" class="form-label">Favorite Cuisine:</label>
              <input 
                type="text" 
                id="favCuisine" 
                v-model="profile.fav_cuisine" 
                class="form-control" 
                required
              />
            </div>
            
            <div class="col-md-6 mb-3">
              <label for="favColour" class="form-label">Favorite Color:</label>
              <input 
                type="text" 
                id="favColour" 
                v-model="profile.fav_colour" 
                class="form-control" 
                required
              />
            </div>
            
            <div class="col-md-6 mb-3">
              <label for="favSchoolSubject" class="form-label">Favorite School Subject:</label>
              <input 
                type="text" 
                id="favSchoolSubject" 
                v-model="profile.fav_school_sibject" 
                class="form-control" 
                required
              />
            </div>
            
            <div class="col-md-6 mb-3 d-flex flex-column">
              <label class="form-label">Preferences:</label>
              
              <div class="form-check">
                <input 
                  type="checkbox" 
                  id="political" 
                  v-model="profile.political" 
                  class="form-check-input"
                />
                <label for="political" class="form-check-label">Political</label>
              </div>
              
              <div class="form-check">
                <input 
                  type="checkbox" 
                  id="religious" 
                  v-model="profile.religious" 
                  class="form-check-input"
                />
                <label for="religious" class="form-check-label">Religious</label>
              </div>
              
              <div class="form-check">
                <input 
                  type="checkbox" 
                  id="familyOriented" 
                  v-model="profile.family_oriented" 
                  class="form-check-input"
                />
                <label for="familyOriented" class="form-check-label">Family Oriented</label>
              </div>
            </div>
          </div>
          
          <div class="alert alert-danger" v-if="error">
            {{ error }}
          </div>
          
          <div class="d-grid gap-2 col-md-6 mx-auto mt-4">
            <button type="submit" class="btn btn-primary">Create Profile</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import apiService from '@/services/api'

export default {
  name: 'NewProfile',
  data() {
    return {
      profile: {
        description: '',
        parish: '',
        biography: '',
        sex: '',
        race: '',
        birth_year: new Date().getFullYear() - 20,
        height: 65,
        fav_cuisine: '',
        fav_colour: '',
        fav_school_sibject: '',
        political: false,
        religious: false,
        family_oriented: false
      },
      currentYear: new Date().getFullYear(),
      error: null
    }
  },
  methods: {
  async createProfile() {
  try {
    this.error = null
    const response = await apiService.createProfile(this.profile)
    
    
    alert('Profile created successfully!')
    
    const user = JSON.parse(localStorage.getItem('user') || '{}')
    
    window.dispatchEvent(new Event('refresh-profiles'))
    
    this.$router.push('/')
  } catch (error) {
    this.error = error.response?.data?.error || 'Failed to create profile. Please try again.'
  }
}
}
}
</script>