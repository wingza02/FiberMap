<template>
  <div>
      <gmap-map :center="center" :zoom="16" mapTypeId="hybrid" style="width: 65%; height: 550px; float: left;">
        <gmap-marker
            :position="marker.position"
            :clickable="false"
            :draggable="true"
            @dragend="posMarker">
        </gmap-marker>
      </gmap-map>
      <div style="display: inline-block; margin-left: 10px; width: 30%">       
        <form @submit.prevent="onSubmit()">
          <div class="form-group" :class="{error: errors.has('Name')}">
              <label for="Name" class="control-label">Name : </label>
              <input name="Name" id="ip" v-model="marker.name" type="text" class="form-control" placeholder="e.g. ITSC" v-validate="'required'"/>
              <span style="color:red" v-show="errors.has('Name')" class="alert alert-danger">{{ errors.first('Name') }}</span>
          </div>
          <div class="form-group" :class="{error: errors.has('Type Node')}">
          <label for="typeNode">Type Node : </label>
          <select class="form-control" v-model="isCore" name="Type Node" id="typeNode" v-validate="'required'">
              <option value="0">Minor Node</option>
              <option value="1">Major Node</option>
          </select>
          <span style="color:red" v-show="errors.has('Type Node')" class="alert alert-danger">{{ errors.first('Type Node') }}</span>
          </div>
          <div class="form-group" :class="{error: errors.has('Zone')}">
          <label for="Zone">Zone : </label>
          <select class="form-control" v-model="zone" name="Zone" id="Zone" v-validate="'required'">
              <option value="COM">COM</option>
              <option value="ENG">ENG</option>
              <option value="AGR">AGR</option>
              <option value="MED">MED</option>
              <option value="MAEHEA">MAE-HEA</option>
          </select>
          <span style="color:red" v-show="errors.has('Zone')" class="alert alert-danger">{{ errors.first('Zone') }}</span>
          </div>
          <div class="form-group">
              <label for="lat">Latitude : </label>
              <input v-model="marker.position.lat" type="text" class="form-control" placeholder="Latitude" readonly />
          </div>
          <div class="form-group">
              <label for="lag">Longitude : </label>
              <input v-model="marker.position.lng" type="text" class="form-control" placeholder="Longitude" readonly />
          </div>
          <hr>
          <button class="btn btn-primary" style="float: right;">Submit</button>
        </form>
        <button class="btn btn-danger" @click="goBack()">Back</button>
      </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      marker: {
        position: {
          lat: 18.79686,
          lng: 98.9537475
        }
      },
      isCore: null,
      zone: null,
      center: { lat: 18.79686, lng: 98.9537475 },
      user: []
    }
  },
  methods: {
    onSubmit() {                                       // Validate input before run sendData()
      const result = this.$validator.validateAll();
      const err = this.errors.items
      if (typeof result.then === 'function') {
        result.then(valid => {
          if(valid === true) {
            this.sendData()
          } else {
            // alert('Please fill in all information.')
            alert(err[0].msg)
          }
        });
      }
    },
    posMarker (position) {                                       // Update Marker Position When Drag Marker
      this.marker.position.lat = position.latLng.lat()
      this.marker.position.lng = position.latLng.lng()
      this.center.lat = this.marker.position.lat
      this.center.lng = this.marker.position.lng
    },
    getDataUser () {                                       // Auth user for each page
      this.user.id = sessionStorage.getItem('iduser')
      this.user.username = sessionStorage.getItem('username')
      this.user.firstname = sessionStorage.getItem('firstname')
      this.user.lastname = sessionStorage.getItem('lastname')
      this.user.tel = sessionStorage.getItem('tel')
      this.user.email = sessionStorage.getItem('email')
      this.user.isAdmin = sessionStorage.getItem('isAdmin') === 'true'
      this.user.isLogin = sessionStorage.getItem('isLogin') === 'true'
      
      this.axios.post('https://fibermap-api.cmu.ac.th/checktoken', {
        token : sessionStorage.getItem('token')
      })
      .then(response => {
        if(response.data.status == 'timeout') {
          this.$router.push({name: 'Login'})
        }
      })
    },
    sendData () {                                       // send data to DB
      this.axios.get('https://fibermap-api.cmu.ac.th/addnode', {
        params: {
          name: this.marker.name,
          lat: parseFloat(this.marker.position.lat).toFixed(7),
          lng: parseFloat(this.marker.position.lng).toFixed(7),
          is_core: this.isCore,
          zone: this.zone
        },
        headers: {'Authorization': sessionStorage.getItem('token')}
      })
        .then(response => {
          window.alert('Added node success.')
          this.$router.push({name: 'Config'})
        })
    },
    goBack () {                                       // go back to config page
      this.$router.push({name: 'Config'})
    }
  },
  created () {                                       // Run these function when start page
    this.getDataUser()
    if (this.user.isAdmin !== true) {
      this.$router.push({name: 'Dashboard'})
    }
  }
}
</script>

<style>
span.error {
  color: #9F3A38;
}
</style>

