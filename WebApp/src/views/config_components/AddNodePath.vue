<template>
  <div>
      <gmap-map @click="addMarker" :center="center" :zoom="16" mapTypeId="hybrid" style="width: 65%; height: 550px; float: left;">
        <gmap-marker
            v-for="(m, index) in marker"
            :key="m.index"
            :position="m.position"
            :clickable="false"
            :draggable="true"
            @dragstart="checkSamePos"
            @dragend="replacePos">
        </gmap-marker>
        <gmap-polyline
            v-for="(pl,index) in paths" 
            :key="index" 
            :path="pl.path"
            :draggable="false"
            :editable="false"
            :options="{geodesic:true, strokeColor:colorline ,strokeWeight:4}">
        </gmap-polyline>
      </gmap-map>
      <div style="display: inline-block; margin-left: 10px; width: 34%">
        <form @submit.prevent="onSubmit()">
          <div class="form-group">
                <div class="form-group">
                  <label for="colorline">Color Line : </label>
                  <color-picker v-model="colorline"></color-picker>
                </div>
              </div>
          <hr>
          <button type="submit" class="btn btn-primary" style="float: right;">Submit</button>
        </form>
          <button class="btn btn-danger" @click="goBack()">Back</button>
          <button class="btn btn-danger" @click="reset()" style="float: right;">Reset</button>
      </div>
  </div>
</template>

<script>
// Import other function from .. file
import colorPicker from '../components/colorPicker'
export default {
  components: {
    colorPicker
  },
  data() {
    return {
      marker: {
        position: {
          lat: 18.79686,
          lng: 98.9537475
        }
      },
      paths: [
        {
          path: []
        }
      ],
      addPath: [
        {
          path: []
        }
      ],
      polyline: {},
      isCore: 0,
      center: { lat: 18.79686, lng: 98.9537475 },
      user: [],
      message: "",
      checkPos: -1,
      lastPos: [
          {
              path: []
          }
      ],
      colorline: 'Black',
    };
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
    addMarker (pos){                                       // add sub-path on polyline with marker
        let position = {position: {lat:parseFloat(pos.latLng.lat().toFixed(7)),lng:parseFloat(pos.latLng.lng().toFixed(7))}}
        this.marker.push(position)
        this.paths[0].path.splice(-1, 0, {
              lat: parseFloat(pos.latLng.lat().toFixed(7)),
              lng: parseFloat(pos.latLng.lng().toFixed(7))
            });
        this.message = JSON.stringify(this.paths[0].path)

    },
    replacePos (pos) {                                       // replace position value when drag marker
      // console.log(this.lastPos[0].path)
      for(let i=0; i<this.paths[0].path.length; i++) {
          if(this.lastPos[0].path.lat == this.paths[0].path[i].lat && this.lastPos[0].path.lng == this.paths[0].path[i].lng) {
              this.paths[0].path[i].lat = parseFloat(pos.latLng.lat().toFixed(7))
              this.paths[0].path[i].lng = parseFloat(pos.latLng.lng().toFixed(7))
              // this.marker[i].position.lat = parseFloat(pos.latLng.lat().toFixed(7))
              // this.marker[i].position.lng = parseFloat(pos.latLng.lng().toFixed(7))
              // console.log('replace')
          }
          this.render()
          this.message = JSON.stringify(this.paths[0].path)
      }
    },
    checkSamePos (pos) {                                       // check position when drag marker
        for(let i=0; i<this.paths[0].path.length; i++) {
            if(parseFloat(pos.latLng.lat().toFixed(7)) == this.paths[0].path[i].lat && parseFloat(pos.latLng.lng().toFixed(7)) == this.paths[0].path[i].lng) {
                // console.log('same')
                this.lastPos[0].path = {lat:parseFloat(pos.latLng.lat().toFixed(7)),lng:parseFloat(pos.latLng.lng().toFixed(7))}
                break
                // console.log(parseFloat(pos.latLng.lat().toFixed(7)))
                // console.log(this.addPath[0].path[i].lat)
                // this.samePos[0].path = {lat:parseFloat(pos.latLng.lat().toFixed(7)),lng:parseFloat(pos.latLng.lng().toFixed(7))}
                // console.log(this.samePos[0])
            }
        }
    },
    render () {                                       // Update Map when Add Marker or Replace Position
        this.addPath[0].path = this.paths[0].path
        this.paths[0].path = []
        for (let i = 0; i < this.addPath[0].path.length; i++) {
            this.paths[0].path.push({
              lat: this.addPath[0].path[i].lat,
              lng: this.addPath[0].path[i].lng
            });
          }
    },
    sendData() {                                       // send data to DB
      // console.log('1')
      this.axios.post('https://fibermap-api.cmu.ac.th/addnodepath', {
        path: this.paths[0].path,
        line_id: this.$route.params.id,
        colorline: this.colorline,
        token : sessionStorage.getItem('token')
      })
        .then(function (response) {
            console.log(response.data)
            alert('Added node path success.')
            this.$router.push({name: 'Config'})
        }.bind(this))
    },
    reset() {                                       // Reset draw line
      this.findNodelatlng();
      this.infoline = []
      this.colorline = 'Black'
    },
    goBack() {                                       // go back to config page
      this.$router.push({ name: "Config" });
    },
    findNodelatlng() {                                       // Get lat and lng of node before draw line
      this.paths[0].path = [];
      this.addPath[0].path = []
      this.axios
        .get("https://fibermap-api.cmu.ac.th/findnodelatlng", {
          params: {
            A: this.$route.params.A,
            B: this.$route.params.B
          },
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
        .then(response => {
          this.marker = response.data;
        //   console.log(this.marker)
          for (let i = 0; i < this.marker.length; i++) {
            this.paths[0].path.push({
              lat: this.marker[i].position.lat,
              lng: this.marker[i].position.lng
            });
          }
          // this.paths[0].path.push({ lat: 18.796137, lng: 98.951652 })
          // console.log(this.addPath[0].path);
          this.center.lat = this.marker[0].position.lat
          this.center.lng = this.marker[0].position.lng
        });
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
  },
  created() {                                       // Run these function when start page
    this.getDataUser();
    if (this.user.isAdmin !== true) {
      this.$router.push({ name: "Dashboard" });
    }
    this.findNodelatlng();
    // console.log(this.$route.params)
  },
};
</script>