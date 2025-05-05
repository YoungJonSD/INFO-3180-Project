// components/SearchForm.vue
<template>
  <div class="search-form mb-4">
    <div class="card">
      <div class="card-header bg-light">
        <h3 class="mb-0">Search</h3>
      </div>
      <div class="card-body">
        <form @submit.prevent="search">
          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="name" class="form-label">Name:</label>
              <input 
                type="text" 
                id="name" 
                v-model="searchParams.name" 
                class="form-control"
              />
            </div>
            
            <div class="col-md-6 mb-3">
              <label for="birthYear" class="form-label">Birth Year:</label>
              <input 
                type="number" 
                id="birthYear" 
                v-model="searchParams.birth_year" 
                class="form-control" 
                min="1900" 
                :max="currentYear"
              />
            </div>
            
            <div class="col-md-6 mb-3">
              <label for="sex" class="form-label">Sex:</label>
              <select 
                id="sex" 
                v-model="searchParams.sex" 
                class="form-select"
              >
                <option value="">Any</option>
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
                v-model="searchParams.race" 
                class="form-control"
              />
            </div>

            <div class="col-md-6 mb-3">
              <label for="parish" class="form-label">Parish:</label>
              <select 
                id="parish" 
                v-model="searchParams.parish" 
                class="form-select"
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
          </div>
          
          <div class="d-grid mt-3">
            <button type="submit" class="btn btn-primary">Search</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SearchForm',
  data() {
    return {
      searchParams: {
        name: '',
        birth_year: null,
        sex: '',
        race: '',
        parish: ''
      },
      currentYear: new Date().getFullYear()
    }
  },
  methods: {
    search() {
      const params = {}
      Object.keys(this.searchParams).forEach(key => {
        if (this.searchParams[key] !== '' && this.searchParams[key] !== null) {
          params[key] = this.searchParams[key]
        }
      })
      
      this.$emit('search', params)
    }
  }
}
</script>