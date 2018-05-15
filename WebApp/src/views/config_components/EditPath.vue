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
              <!-- <button class="btn btn-primary" type="button" data-toggle="collapse" data-target="#info" aria-expanded="false" aria-controls="collapseExample">
                Infomation
              </button>
              <button class="btn btn-primary" type="button" data-toggle="collapse" data-target="#polyline" aria-expanded="false" aria-controls="collapseExample">
                Polyline
              </button> -->
            <!-- <div class="collapse" id="info">
              <div class="card card-body"> -->
                <div class="form-group" :class="{error: errors.has('Type Mode')}">
                  <label for="typeline" class="control-label">Type Mode : </label>
                  <select name="Type Mode" id="typeline" class="form-control" v-model="infoline.type_id" v-validate="'required'">
                      <option value="1">Single Mode</option>
                      <option value="2">Multi Mode</option>
                      <option value="3">UTP</option>
                  </select>
                  <span style="color:red" v-show="errors.has('Type Mode')" class="alert alert-danger">{{ errors.first('Type Mode') }}</span>
                </div>
                <div class="form-group">
                  <label for="colorline">Color Line : </label>
                  <select class="form-control" v-model="colorline">
                      <option value="Green">Green</option>
                      <option value="Blue">Blue</option>
                      <option value="DarkOrange">DarkOrangee</option>
                      <option value="Aqua">Aqua</option>
                      <option value="BlueViolet">BlueViolet</option>
                      <option value="LightGray">LightGray</option>
                      <option value="LightPink">LightPink</option>
                      <option value="LightSalmon">LightSalmon</option>
                      <option value="Black">Black</option>
                  </select>
                </div>
                <div class="form-group" :class="{error: errors.has('Distance')}">
                  <label for="distance" class="control-label">Distance (Unit = Meter) : </label>
                  <input name="Distance" id="distance" v-model="infoline.distance" type="text" class="form-control" placeholder="e.g. 205.45" v-validate="'required|numeric'" />
                  <span style="color:red" v-show="errors.has('Distance')" class="alert alert-danger">{{ errors.first('Distance') }}</span>
                </div>
                <div class="form-group">
                  <label for="gmapdistance" class="control-label">GoogleMap Distance (Unit = Meter) : </label>
                  <input name="gmapDistance" id="gmapdistance" v-model="infoline.gmap_distance" type="text" class="form-control" readonly />
                </div>
                <div class="form-group" :class="{error: errors.has('Core Number')}">
                  <label for="core" class="control-label">Core Number : </label>
                  <input name="Core Number" id="core" v-model="infoline.core" type="text" class="form-control" placeholder="e.g. 12" v-validate="'required|numeric'"/>
                  <span style="color:red" v-show="errors.has('Core Number')" class="alert alert-danger">{{ errors.first('Core Number') }}</span>
                </div>
                <div class="form-group" :class="{error: errors.has('Patch')}">
                  <label for="patch" class="control-label">Patch : </label>
                  <input name="Patch" id="patch" v-model="infoline.patch" type="text" class="form-control" placeholder="e.g. 1,2" v-validate="'required'"/>
                  <span style="color:red" v-show="errors.has('Patch')" class="alert alert-danger">{{ errors.first('Patch') }}</span>
                </div>
                <div class="form-group" :class="{error: errors.has('Connector')}">
                  <label for="connector" class="control-label">Connector : </label>
                  <input name="Connector" id="connector" v-model="infoline.connector" type="text" class="form-control" placeholder="e.g. LC-SC" v-validate="'required'"/>
                  <span style="color:red" v-show="errors.has('Connector')" class="alert alert-danger">{{ errors.first('Connector') }}</span>
                </div>
              </div>
            <!-- </div> -->

            <!-- <div class="collapse" id="polyline">
              <div class="card card-body">
                <label for="exampleFormControlTextarea1">PolyLine Coordinate</label>
                <textarea class="form-control" id="exampleFormControlTextarea1" rows="10" v-model="message" disabled></textarea>
              </div>
            </div>
          </div> -->
            <!-- <label for="exampleFormControlTextarea1">PolyLine Coordinate</label>
            <textarea class="form-control" id="exampleFormControlTextarea1" rows="10" v-model="message"></textarea>
          </div> -->
          <!-- <div class="form-group">
              <label for="ip">IP Address : </label>
              <input v-model="marker.ip" type="text" class="form-control" placeholder="e.g. 192.168.1.1" />
          </div>
          <div class="form-group">
          <label for="typeSwitch">Type Switch : </label>
          <select class="form-control" v-model="isCore">
              <option value="0">Edge Switch</option>
              <option value="1">Core Switch</option>
          </select>
          </div>
          <div class="form-group">
              <label for="lat">Latitude : </label>
              <input v-model="marker.position.lat" type="text" class="form-control" placeholder="Latitude" disabled />
          </div>
          <div class="form-group">
              <label for="lag">Longitude : </label>
              <input v-model="marker.position.lng" type="text" class="form-control" placeholder="Longitude" disabled />
          </div> -->
          <hr>
          <button type="submit" class="btn btn-primary" style="float: right;">Submit</button>
        </form>
          <button class="btn btn-danger" @click="goBack()">Back</button>
          <button class="btn btn-warning" @click="reset()" style="float: right;">Reset</button>
          <button class="btn btn-danger" @click="newDraw()" style="float: right;">New Draw</button>
          <!-- <button class="btn btn-primary" @click="backward()" style="float: right;">Backward</button>
          <button class="btn btn-primary" @click="render1()" style="float: right;">Render</button>      
          <button class="btn btn-primary" @click="add()" style="float: right;">Render</button>         -->
      </div>
  </div>
</template>

<script>

export default {
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
      infoline: {
        distance: null,
        gmap_distance: null,
        type_id: null,
        core: null,
        patch: null,
        connector: null
      }
    };
  },
  methods: {
    onSubmit() {
      const result = this.$validator.validateAll();
      const err = this.errors.items
      if (typeof result.then === 'function') {
        result.then(valid => {
          if(valid === true) {
            this.beforeSendData()
          } else {
            // alert('Please fill in all information.')
            alert(err[0].msg)
          }
        });
      }
    },
    addMarker (pos){
        let position = {position: {lat:parseFloat(pos.latLng.lat().toFixed(7)),lng:parseFloat(pos.latLng.lng().toFixed(7))}}
        this.marker.push(position)
        this.paths[0].path.splice(-1, 0, {
              lat: parseFloat(pos.latLng.lat().toFixed(7)),
              lng: parseFloat(pos.latLng.lng().toFixed(7))
            });
        this.calDistance()
        // console.log(this.marker)
        // console.log(position)
        this.message = JSON.stringify(this.paths[0].path)

    },
    replacePos (pos) {
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
      this.calDistance()
    },
    checkSamePos (pos) {
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
    calDistance () {
      let distance = 0
      for (let i = 0; i < this.paths[0].path.length - 1; i++) {
          distance = distance + this.getDistance(this.paths[0].path[i].lat, this.paths[0].path[i].lng, this.paths[0].path[i + 1].lat, this.paths[0].path[i + 1].lng)
        }
      console.log(distance)
      this.infoline.gmap_distance = (distance*1000).toFixed(4)
    },
    getDistance (slat, slng, flat, flng) {
      let R = 6371
      let dLat = (flat - slat) * (Math.PI / 180)
      let dLng = (flng - slng) * (Math.PI / 180)
      let a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(slat * (Math.PI / 180)) * Math.cos(flat * (Math.PI / 180)) *
        Math.sin(dLng / 2) * Math.sin(dLng / 2)
      let c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
      let d = R * c
      return d
    },
    render () {
        this.addPath[0].path = this.paths[0].path
        this.paths[0].path = []
        for (let i = 0; i < this.addPath[0].path.length; i++) {
            this.paths[0].path.push({
              lat: this.addPath[0].path[i].lat,
              lng: this.addPath[0].path[i].lng
            });
          }
    },
    beforeSendData() {
        this.axios.get('https://fibermap.herokuapp.com/deletepath', {
            params: {
                line_id: this.$route.params.id
            }
        })
        .then(response => {
            this.sendData()
        })
    },
    sendData() {
      this.axios.post('https://fibermap.herokuapp.com/addpath', {
        path: this.paths[0].path,
        line_id: this.$route.params.id,
        colorline: this.colorline
      })
        .then(function (response) {
            console.log(response.data)
        })
      this.axios.post('https://fibermap.herokuapp.com/addinfoline', {
        line_id: this.$route.params.id,
        distance: this.infoline.distance,
        gmap_distance: this.infoline.gmap_distance,
        type_id: this.infoline.type_id,
        core: this.infoline.core,
        patch: this.infoline.patch,
        connector: this.infoline.connector
      })
        .then(function (response) {
            console.log(response.data)
            alert('Edited path success.')
            this.$router.push({name: 'Config'})
        }.bind(this))
    },
    reset() {
      this.getPath()
      this.getInfoline()
    },
    newDraw () {
        this.findlatlng();
        this.infoline.distance = null
        this.infoline.type_id = null
        this.infoline.core = null
        this.infoline.patch = null
        this.infoline.connector = null
        this.colorline = 'Black'
    },
    goBack() {
      this.$router.push({ name: "Config" });
    },
    findlatlng() {
      this.paths[0].path = [];
      this.addPath[0].path = []
      this.axios
        .get("https://fibermap.herokuapp.com/findlatlng", {
          params: {
            A: this.$route.params.A,
            B: this.$route.params.B
          }
        })
        .then(response => {
          this.marker = response.data;
          console.log(this.marker)
          for (let i = 0; i < this.marker.length; i++) {
            this.paths[0].path.push({
              lat: this.marker[i].position.lat,
              lng: this.marker[i].position.lng
            });
          }
          this.calDistance()
          // this.paths[0].path.push({ lat: 18.796137, lng: 98.951652 })
        //   console.log(this.addPath[0].path);
        });
    },
    getInfoline () {
        this.axios.get('https://fibermap.herokuapp.com/getinfoline', {
        params: {
            line_id: this.$route.params.id
        }
      })
        .then(response => {
            // console.log(response.data)
            // console.log(this.infoline.distance)
            this.infoline.distance = response.data.distance
            this.infoline.gmap_distance = response.data.gmap_distance
            if (response.data.type == 'Single Mode') {
                this.infoline.type_id = 1
            } else if (response.data.type == 'Multi Mode') {
                this.infoline.type_id = 2
            } else if (response.data.type == 'UTP') {
                this.infoline.type_id = 3
            }
            this.infoline.core = response.data.core_number
            this.infoline.patch = response.data.patch
            this.infoline.connector = response.data.connector
            // console.log(this.infoline)
        })
    },
    getPath () {
        this.axios.get('https://fibermap.herokuapp.com/getpathedit', {
        params: {
            line_id: this.$route.params.id
        }
      })
        .then(response => {
            this.marker = []
            this.paths[0].path = []
            // console.log(response.data)
            for(let i=0; i<response.data.length; i++) {
                this.marker.push({position: {lat:response.data[i].lat, lng:response.data[i].lng}})
            }
            for (let i = 0; i < this.marker.length; i++) {
              this.paths[0].path.push({
                lat: this.marker[i].position.lat,
                lng: this.marker[i].position.lng
              });
            }
            this.colorline = response.data[0].colorline
            // console.log(this.marker)
            this.center.lat = this.marker[0].position.lat
            this.center.lng = this.marker[0].position.lng
        })
    },
    getDataUser() {
      this.user.id = sessionStorage.getItem("iduser");
      this.user.username = sessionStorage.getItem("username");
      this.user.firstname = sessionStorage.getItem("firstname");
      this.user.lastname = sessionStorage.getItem("lastname");
      this.user.tel = sessionStorage.getItem("tel");
      this.user.email = sessionStorage.getItem("email");
      this.user.isAdmin = sessionStorage.getItem("isAdmin") === "true";
      this.user.isLogin = sessionStorage.getItem("isLogin") === "true";
    },
  },
  created() {
    this.getDataUser();
    if (this.user.isAdmin !== true) {
      this.$router.push({ name: "Dashboard" });
    }
    // this.findlatlng();
    this.getPath()
    this.getInfoline()
    // console.log(this.$route.params)
  },
};
</script>