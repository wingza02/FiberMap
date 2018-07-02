<template>
  <div>
      <gmap-map :center="marker.position" :zoom="16" mapTypeId="hybrid" style="width: 65%; height: 550px; float: left;">
        <gmap-marker
            :position="marker.position"
            :clickable="false"
            :draggable="true"
            @dragend="posMarker">
        </gmap-marker>
      </gmap-map>
      <div style="display: inline-block; margin-left: 10px; width: 30%">
        <form @submit.prevent="onSubmit()">
              <div class="form-group">
                <label for="name">Name Switch : </label>
                <input v-model="marker.name" type="text" class="form-control" readonly />
            </div>
            <div class="form-group" :class="{error: errors.has('IP Address')}">
              <label for="ip" class="control-label">IP Address : </label>
              <input name="IP Address" id="ip" v-model="marker.ip" type="text" class="form-control" placeholder="e.g. 192.168.1.1" v-validate="'required|ip'"/>
              <span style="color:red" v-show="errors.has('IP Address')" class="alert alert-danger">{{ errors.first('IP Address') }}</span>
            </div>
            <div class="form-group" :class="{error: errors.has('Model Switch')}">
            <label for="ModelSwitch">Model Switch : </label>
            <select class="form-control" v-model="marker.model" name="Model Switch" id="ModelSwitch" v-validate="'required'">
                <option v-for="m in model" :key="m.id">{{m.model}}</option>
            </select>
            <span style="color:red" v-show="errors.has('Model Switch')" class="alert alert-danger">{{ errors.first('Model Switch') }}</span>
            </div>
            <div class="form-group">
            <label for="typeSwitch">Type Switch : </label>
            <select class="form-control" v-model="marker.is_core">
                <option value="0">Edge Switch</option>
                <option value="1">Core Switch</option>
            </select>
            </div>
            <div class="form-group">
                <label for="lat">Latitude : </label>
                <input v-model="marker.position.lat" type="text" class="form-control" placeholder="Latitude" readonly />
            </div>
            <div class="form-group">
                <label for="lag">Longitude : </label>
                <input v-model="marker.position.lat" type="text" class="form-control" placeholder="Longitude" readonly />
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
      marker: [],
      user: [],
      model: []
    }
  },
  methods: {
    onSubmit() {                                       // Validate input before run sendData()
      const result = this.$validator.validateAll()
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
      this.axios.get('https://fibermap-api.cmu.ac.th/editswitch', {
        params: {
          id_ip: this.marker.id_ip,
          ip: this.marker.ip,
          lat: parseFloat(this.marker.position.lat).toFixed(7),
          lng: parseFloat(this.marker.position.lng).toFixed(7),
          is_core: this.marker.is_core,
          model: this.marker.model
        },
        headers: {'Authorization': sessionStorage.getItem('token')}
      })
        .then(response => {
          window.alert('Edited switch success.')
          this.$router.push({name: 'Config'})
        })
    },
    goBack () {                                       // go back to config page
      this.$router.push({name: 'Config'})
    },
    getModel() {                                       // Get Model Switch From DB
      this.axios.get('https://fibermap-api.cmu.ac.th/getmodel', {
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
      .then(response => {
        this.model = response.data
      })
    }
  },
  created () {                                       // Run these function when start page
    this.getDataUser()
    this.getModel()
    if (this.user.isAdmin !== true) {
      this.$router.push({name: 'Dashboard'})
    }
    this.marker = this.$route.params
    this.marker.id_ip = this.$route.params.ip
  }
}
</script>
