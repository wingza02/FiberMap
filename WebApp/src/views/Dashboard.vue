<template>
  <div class="animated fadeIn">
    <b-row>
<!-- Switch Block -->
      <b-col sm="6" lg="4">
        <b-card no-body class="bg-primary" :no-body="true">
          <b-card-body class="pb-0">
            <h2>Status Switch</h2>
            <h3 class="mb-0">Up: {{ upSw }}</h3>
            <h3 class="mb-0">Down: {{ downSw }}</h3>
            <h4>
            <li v-for="(sw,index) in switchs" :key="index">
              {{ sw.name }}
            </li></h4>
          </b-card-body>
        </b-card>
      </b-col>

<!-- Line Block -->
      <b-col sm="6" lg="4">
        <b-card no-body class="bg-danger" :no-body="true">
          <b-card-body class="pb-0">
            <h2>Status Line</h2>
            <h3 class="mb-0">Up: {{ upLine }}</h3>
            <h3 class="mb-0">Down: {{ downLine }}</h3>
            <h4>
            <li v-for="(line,index) in connects" :key="index">
              <a  @click="linkTo(line)" style="cursor: pointer; color:blue;" >{{ line.A }} - {{ line.B }}</a>
            </li></h4>
          </b-card-body>
        </b-card>
      </b-col>

<!-- Interface Block -->
      <b-col sm="6" lg="4">
        <b-card no-body class="bg-secondary" :no-body="true">
          <b-card-body class="pb-0">
            <h2>Status Interface</h2>
            <h3 class="mb-0">Up: {{ upIf }}</h3>
            <h3 class="mb-0">Down: {{ downIf }}</h3>
            <h4>
            <li v-for="(port,index) in interfaces" :key="index">
              {{ port.name }} - {{ port.type }}
            </li></h4>
          </b-card-body>
        </b-card>
      </b-col>
    </b-row> 
    
<!-- Announce Block -->
    <b-row>
      <b-col sm="6" lg="4">
        <b-card no-body class="bg-secondary" :no-body="true">
          <b-card-body class="pb-0">
            <h2>Announce</h2>
            <!-- <h3 class="mb-0">Up: {{ upSw }}</h3> -->
            <!-- <h3 class="mb-0">Down: {{ downSw }}</h3> -->
            <h4>
            <li v-for="(an,index) in announce" :key="index">
              <a  @click="linkTo(an)" style="cursor: pointer; color:blue;" >{{ an.A }} - {{ an.B }}</a>
            </li></h4>
          </b-card-body>
        </b-card>
      </b-col>

<!-- Maintenance Block -->
      <b-col sm="6" lg="4">
        <b-card no-body class="bg-warning" :no-body="true">
          <b-card-body class="pb-0">
            <h2>Maintenance</h2>
            <!-- <h3 class="mb-0">Up: {{ upLine }}</h3>
            <h3 class="mb-0">Down: {{ downLine }}</h3> -->
            <h4>
            <li v-for="(mt,index) in maintain" :key="index">
              <a  @click="linkTo(mt)" style="cursor: pointer; color:blue;" >{{ mt.A }} - {{ mt.B }}</a>
            </li></h4>
          </b-card-body>
        </b-card>
      </b-col>

<!-- Confirm Block -->
      <b-col sm="6" lg="4">
        <b-card no-body class="bg-success" :no-body="true">
          <b-card-body class="pb-0">
            <h2>Wait for Confirm</h2>
            <!-- <h3 class="mb-0">Up: {{ upLine }}</h3>
            <h3 class="mb-0">Down: {{ downLine }}</h3> -->
            <h4>
            <li v-for="(cf,index) in confirm" :key="index">
              <a  @click="linkTo(cf)" style="cursor: pointer; color:blue;" >{{ cf.A }} - {{ cf.B }}</a>
            </li></h4>
          </b-card-body>
        </b-card>
      </b-col>
    </b-row> 
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  data: function () {
    return {
      switchs: [],
      connects: [],
      interfaces: [],
      upSw: 0,
      downSw: 0,
      upLine: 0,
      downLine: 0,
      upIf: 0,
      downIf: 0,
      position: {
        lat: 0,
        lng: 0
      },
      history: [],
      announce: [],
      maintain: [],
      confirm: [],
      allConnect: [],
      timer: 0,
      user: []
    }
  },
  methods: {
    findBreak () {                                       // Show break line status on each block
      this.announce = []
      this.maintain = []
      this.confirm = []
      // console.log(this.connects.length)
      // console.log(this.history.length)
      for(let i=0; i<this.allConnect.length; i++) {
        for(let j=0; j<this.history.length; j++) {
          if ( this.allConnect[i].id == this.history[j].line_id) {
            if(this.history[j].status_broken == 1) {
              this.announce.push(this.allConnect[i])
            }
            if(this.history[j].status_broken == 2) {
              this.maintain.push(this.allConnect[i])
            }
            if(this.history[j].status_broken == 3) {
              this.confirm.push(this.allConnect[i])
            }
          }
        }
      }
    },
    linkTo (line) {                                       // Go to MaptoReal Page for focus that path
      this.position.lat = line.path[0].lat
      this.position.lng = line.path[0].lng
      // console.log(this.$route)
      let hostname
      let protocol = location.protocol
      if (location.hostname === 'localhost') {
        hostname = location.host
      } else {
        hostname = location.hostname
      }
      // this.$router.push({name: 'Map', params: {'lineid': lineid, 'lat': this.position.lat, 'lng': this.position.lng}})
      location.href = '' + protocol + '//' + hostname + '/#/maptoreal?lineid=' + line.id + '&lat=' + this.position.lat + '&lng=' + this.position.lng
      // console.log(this.infoContent.id)
    },
    getSwitch () {                                       // Get switch from DB
      this.switchs = []
      this.upSw = 0
      this.downSw = 0
      this.axios
        .get('https://fibermap-api.cmu.ac.th/getswitch', {
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
        .then(response => {
          // console.log(response.data)
          response.data.forEach(element => {
            if (element.status === 'Up') {
              this.upSw++
            } else {
              this.downSw++
              this.switchs.push(element)
            }
          })
        })
    },
    getConnect () {                                       // Get path from DB
      this.connects = []
      this.upLine = 0
      this.downLine = 0
      this.axios
        .get('https://fibermap-api.cmu.ac.th/connect', {
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
        .then(response => {
          // console.log(response.data)
          // this.connects = response.data
          this.allConnect = response.data
          response.data.forEach(element => {
            if (element.linestatus === 'Up') {
              this.upLine++
            } else {
              this.downLine++
              this.connects.push(element)
            }
          })
          // console.log(this.allConnect)
          this.getHistory()
        })
    },
    getInterface () {                                       // Get interface from DB
      this.interfaces = []
      this.upIf = 0
      this.downIf = 0
      this.axios
        .get('https://fibermap-api.cmu.ac.th/interface', {
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
        .then(response => {
          response.data.forEach(element => {
            // console.log(element)
            if (element.status === 1) {
              this.upIf++
            } else {
              this.downIf++
              this.interfaces.push(element)
            }
          })
        })
    },
    getHistory () {                                       // Get history path from DB
      this.axios.get('https://fibermap-api.cmu.ac.th/gethistory', {
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
      .then(response => {
        this.history = response.data.data
        // console.log(this.history.length)
        this.findBreak()
      })
    },
    reloadData () {                                       // Refresh page
      this.getSwitch()
      this.getConnect()
      this.getInterface()
    },
    timerReload () {                                       // Timer Refresh Page
      this.timer = setInterval(this.reloadData, 300000) // unit = msec || 1000 = 1sec
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
    }
  },
  created () {                                       // Run these function when start page
    this.reloadData()
    this.timerReload()
    this.getDataUser()
    // console.log(window.screen.height)
    // console.log(window.screen.width)
  },
}
</script>
