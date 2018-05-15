<template>
  <div>
<!-- ############################################################################################### -->
    <h2>Switch Management</h2>
    <p>
      <button class="btn btn-primary" @click="gotoAddSwitch()">Add Switch</button>
       <button class="btn btn-warning" type="button" data-toggle="collapse" data-target="#editswitch" aria-expanded="false" aria-controls="collapseExample" @click="getSwitch()">
          Modify Switch
      </button>
      <!-- <button class="btn btn-primary" type="button" data-toggle="collapse" data-target="#deleteswitch" aria-expanded="false" aria-controls="collapseExample" @click="getSwitch()">
          Delete Switch
      </button> -->
      <button class="btn btn-danger" type="button" data-toggle="collapse" data-target="#deleteIP" aria-expanded="false" aria-controls="collapseExample" @click="getIp()">
          Manage IP Address
      </button>
    </p>
    <div class="collapse" id="editswitch">
      <div class="card card-body">
        <h3>Search : <input v-model="search" type="text" placeholder="Search by Name Switch" /></h3> <hr>
          <div v-for="sw in filterSwitch" :key="sw.index">
              <h4>{{sw.id}}. {{ sw.name }} - {{ sw.ip }} || <button class="btn btn-warning" @click="gotoModifySwitch(sw)">Edit</button></h4>
          </div>
      </div>
    </div>
    <!-- <div class="collapse" id="deleteswitch">
      <div class="card card-body">
          <div v-for="sw in switchs" :key="sw.index">
              <h4>{{sw.id}}. {{ sw.name }} - <button class="btn btn-danger" @click="deleteSwitch(sw.name)">Delete</button></h4>
          </div>
      </div>
    </div> -->
    <div class="collapse" id="deleteIP">
      <div class="card card-body">
        <h3>Search : <input v-model="search" type="text" placeholder="Search by IP" /></h3> <hr>
          <div v-for="ip in filterIP" :key="ip.index">
              <h4>{{ip.id}}. {{ ip.ip }} || <button class="btn btn-danger" @click="deleteIp(ip.ip)">Delete</button></h4>
          </div>
      </div>
    </div>
    <hr>
<!-- ############################################################################################### -->
    <h2>Path Management</h2>
    <p>
      <button class="btn btn-primary" type="button" data-toggle="collapse" data-target="#addpath" aria-expanded="false" aria-controls="collapseExample" @click="getNullPath()">
          Add Path
      </button>
      <button class="btn btn-warning" type="button" data-toggle="collapse" data-target="#editpath" aria-expanded="false" aria-controls="collapseExample" @click="getPath()">
          Modify Path
      </button>
      <button class="btn btn-danger" type="button" data-toggle="collapse" data-target="#deletepath" aria-expanded="false" aria-controls="collapseExample" @click="getPath()">
          Delete Path
      </button>
    </p>
    <div class="collapse" id="addpath">
      <div class="card card-body">
          <h3>Search : <input v-model="search" type="text" placeholder="Search by Destination" /></h3> <hr>
          <div v-for="path in filterPath" :key="path.index">
              <h4>From : {{ path.A }} - To : {{ path.B }} || <button class="btn btn-primary" @click="gotoAddPath(path)">Add</button></h4>
          </div>
      </div>
    </div>
    <div class="collapse" id="editpath">
      <div class="card card-body">
        <h3>Search : <input v-model="search" type="text" placeholder="Search by Destination" /></h3> <hr>
          <div v-for="path in filterPath" :key="path.index">
              <h4>From : {{ path.A }} - To : {{ path.B }} || <button class="btn btn-warning" @click="gotoEditPath(path)">Edit</button></h4>
          </div>
      </div>
    </div>
    <div class="collapse" id="deletepath">
      <div class="card card-body">
        <h3>Search : <input v-model="search" type="text" placeholder="Search by Destination" /></h3> <hr>
          <div v-for="path in filterPath" :key="path.index">
              <h4>From : {{ path.A }} - To : {{ path.B }} || <button class="btn btn-danger" @click="deletePath(path)">Delete</button></h4>
          </div>
      </div>
    </div>
    <hr>
<!-- ############################################################################################### -->
    <h2>User Management</h2>
    <p>
      <button class="btn btn-primary" @click="gotoAddUser()">Add User</button>
      <button class="btn btn-warning" type="button" data-toggle="collapse" data-target="#edituser" aria-expanded="false" aria-controls="collapseExample" @click="getUser(0)">
          Modify User
      </button>
      <button class="btn btn-danger" type="button" data-toggle="collapse" data-target="#deleteuser" aria-expanded="false" aria-controls="collapseExample" @click="getUser(1)">
          Delete User
      </button>
    </p>
    <div class="collapse" id="edituser">
      <div class="card card-body">
        <h3>Search : <input v-model="search" type="text" placeholder="Search by Username" /></h3> <hr>
          <div v-for="(iu,index) in filterUser" :key="index">
            <h3>{{iu.username}} - {{ iu.firstname }} || Role: <font v-if="iu.isAdmin==1">Admin</font><font v-else-if="iu.isAdmin==0">Technician</font> <button class="btn btn-primary" @click="gotoEditUser(iu)">Edit Infomation</button> || <button class="btn btn-primary" @click="gotoChangePass(iu)">Change Password</button> </h3>
          </div>
      </div>
    </div>
    <div class="collapse" id="deleteuser">
      <div class="card card-body">
        <h3>Search : <input v-model="search" type="text" placeholder="Search by Username" /></h3> <hr>
          <div v-for="(iu,index) in filterUser" :key="index">
            <h3>{{iu.username}} - {{ iu.firstname }} || Role: <font v-if="iu.isAdmin==1">Admin</font><font v-else-if="iu.isAdmin==0">Technician</font> <button class="btn btn-danger" @click="deleteUser(iu)">Delete</button></h3>
          </div>
      </div>
    </div>
    <!-- <hr> -->
  </div>
</template>

<script>
export default {
  data () {
    return {
      user: [],
      switchs: [],
      ips: [],
      paths: [],
      infouser: [],
      search: ''
    }
  },
  methods: {
    gotoAddSwitch () {
      this.$router.push({name: 'AddSwitch'})
    },
    gotoModifySwitch (data) {
      this.$router.push({name: 'EditSwitch', params: data})
    },
    gotoAddPath (data) {
      this.$router.push({name: 'AddPath', params: data})
    },
    gotoEditPath (data) {
      this.$router.push({name: 'EditPath',params:data})
    },
    gotoAddUser () {
      this.$router.push({name: 'AddUser'})
    },
    gotoEditUser (data) {
      this.$router.push({name: 'EditUser', params:data})
    },
    gotoChangePass(data) {
      this.$router.push({name: 'ChangePass', params:data})
    },
    getDataUser () {
      this.user.id = sessionStorage.getItem('iduser')
      this.user.username = sessionStorage.getItem('username')
      this.user.firstname = sessionStorage.getItem('firstname')
      this.user.lastname = sessionStorage.getItem('lastname')
      this.user.tel = sessionStorage.getItem('tel')
      this.user.email = sessionStorage.getItem('email')
      this.user.isAdmin = sessionStorage.getItem('isAdmin') === 'true'
      this.user.isLogin = sessionStorage.getItem('isLogin') === 'true'
    },
    getSwitch () {
      this.switchs = []
      this.axios
        .get('https://fibermap.herokuapp.com/getswitch')
        .then(response => {
          // console.log(response.data[0].name)
          this.switchs = response.data
        })
    },
    deleteSwitch (data) {
      window.confirm('คุณต้องการลบ : ' + data + ' ?')
    //   function delete switch
    },
    getIp () {
      this.ips = []
      this.axios.get('https://fibermap.herokuapp.com/getip')
        .then(response => {
        //   console.log(response.data[0].name)
          this.ips = response.data
        })
    },
    deleteIp (data) {
      if (confirm('Are you delete :' + data + ' ?') === true) {
        this.axios
          .get('https://fibermap.herokuapp.com/deleteip', {
            params: {
              ip: data
            }
          })
          .then(response => {
            alert('Deleted IP success.')
            location.reload()
          })
      } else {
        console.log('no')
      }
    },
    getNullPath () {
      this.paths = []
      this.axios
        .get('https://fibermap.herokuapp.com/getrealpath')
        .then(response => {
          this.paths = []
          for (let i = 0; i < response.data.length; i++) {
            if (response.data[i].path.length === 0) {
              this.paths.push(response.data[i])
            }
          }
        //   console.log(this.paths)
        })
    },
    getPath () {
      this.paths = []
      this.axios
        .get('https://fibermap.herokuapp.com/getrealpath')
        .then(response => {
          this.paths = []
          for (let i = 0; i < response.data.length; i++) {
            if (response.data[i].path.length !== 0) {
              this.paths.push(response.data[i])
            }
          }
          // console.log(this.paths)
        })
    },
    deletePath (data) {
      if (confirm('Are you delete : From' + data.A + " to " + data.B + ' ?') === true) {
        this.axios
          .get('https://fibermap.herokuapp.com/deletepath', {
            params: {
              line_id: data.id
            }
          })
          .then(response => {
            alert('Deleted path success.')
            location.reload()
          })
      } else {
        console.log('no')
      }
    },
    getUser (event) {
      this.infouser = []
      this.axios.get('https://fibermap.herokuapp.com/getuser')
      .then(response => {
        // console.log(event)
        console.log(response.data)
        if(event==1) {
          for(let i=0; i<response.data.length; i++) {
            if(this.user.id != response.data[i].id) {
              this.infouser.push(response.data[i])
            }
          }
        } else {
          this.infouser = response.data
        }
      })
    },
    deleteUser (data) {
      if (confirm('Are you delete : ' + data.firstname + "  " + data.lastname + ' ?') === true) {
        this.axios
          .get('https://fibermap.herokuapp.com/deleteuser', {
            params: {
              user_id: data.id
            }
          })
          .then(response => {
            alert('Deleted user success.')
            location.reload()
          })
      } else {
        console.log('no')
      }
    }
  },
  created () {
    this.getDataUser()
    if (this.user.isAdmin !== true) {
      this.$router.push({name: 'Dashboard'})
    }
  },
  computed: {
    filterSwitch () {
      return this.switchs.filter(sw => {
        return sw.name.toLowerCase().match(this.search.toLowerCase())
      })
    },
    filterIP () {
      return this.ips.filter(ip => {
        return ip.ip.match(this.search)
      })
    },
    filterPath () {
      return this.paths.filter(path => {
        return path.B.toLowerCase().match(this.search.toLowerCase())
      })
    },
    filterUser () {
      return this.infouser.filter(user => {
        return user.username.toLowerCase().match(this.search.toLowerCase())
      })
    },
  }
}
</script>
