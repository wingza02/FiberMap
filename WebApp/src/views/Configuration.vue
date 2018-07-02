<template>
  <div>
<!-- ###########################################Switch############################################## -->
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
              <h3>{{sw.id}}. {{ sw.name }} - {{ sw.ip }} || <button class="btn btn-warning" @click="gotoModifySwitch(sw)">Edit</button></h3>
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
              <h3>{{ip.id}}. {{ ip.ip }} - {{ ip.name }} || <button class="btn btn-danger" @click="deleteIp(ip.ip)">Delete</button></h3>
          </div>
      </div>
    </div>
    <hr>
<!-- #############################################Path############################################## -->
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
              <h3>From : {{ path.A }} - To : {{ path.B }} || <button class="btn btn-primary" @click="gotoAddPath(path)">Add</button></h3>
          </div>
      </div>
    </div>
    <div class="collapse" id="editpath">
      <div class="card card-body">
        <h3>Search : <input v-model="search" type="text" placeholder="Search by Destination" /></h3> <hr>
          <div v-for="path in filterPath" :key="path.index">
              <h3>From : {{ path.A }} - To : {{ path.B }} || <button class="btn btn-warning" @click="gotoEditPath(path)">Edit</button></h3>
          </div>
      </div>
    </div>
    <div class="collapse" id="deletepath">
      <div class="card card-body">
        <h3>Search : <input v-model="search" type="text" placeholder="Search by Destination" /></h3> <hr>
          <div v-for="path in filterPath" :key="path.index">
              <h3>From : {{ path.A }} - To : {{ path.B }} || <button class="btn btn-danger" @click="deletePath(path)">Delete</button></h3>
          </div>
      </div>
    </div>
    <hr>
<!-- #############################################User############################################## -->
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
    <hr>
    <!-- ####################################Node Fiber################################################# -->
    <h2>Node Fiber Management</h2>
    <p>
      <button class="btn btn-primary" @click="gotoAddNode()">Add Node</button>
      <button class="btn btn-warning" type="button" data-toggle="collapse" data-target="#editnode" aria-expanded="false" aria-controls="collapseExample" @click="getNode()">
          Modify Node
      </button>
      <button class="btn btn-danger" type="button" data-toggle="collapse" data-target="#deletenode" aria-expanded="false" aria-controls="collapseExample" @click="getNode()">
          Delete Node
      </button>
    </p>
    <div class="collapse" id="editnode">
      <div class="card card-body">
        <h3>Search : <input v-model="search" type="text" placeholder="Search by Name" /></h3> <hr>
          <div v-for="(n,index) in filterNode" :key="index">
            <h3>{{n.id}} - {{n.name}} || <button class="btn btn-warning" @click="gotoEditNode(n)">Edit</button> </h3>
          </div>
      </div>
    </div>
    <div class="collapse" id="deletenode">
      <div class="card card-body">
        <h3>Search : <input v-model="search" type="text" placeholder="Search by Name" /></h3> <hr>
          <div v-for="(n,index) in filterNode" :key="index">
            <h3>{{n.id}} - {{n.name}} || <button class="btn btn-danger" @click="deleteNode(n)">Delete</button> </h3>
          </div>
      </div>
    </div>
    <hr>
    <!-- ###################################Node Connection############################################# -->
    <h2>Node Connection Management</h2>
    <p>
      <button class="btn btn-primary" @click="gotoAddNodeConnect()">Add Node-Connect</button>
      <button class="btn btn-danger" type="button" data-toggle="collapse" data-target="#deletenodeconnect" aria-expanded="false" aria-controls="collapseExample" @click="getNodeConn()">
          Delete Node-Connect
      </button>
    </p>
    <div class="collapse" id="deletenodeconnect">
      <div class="card card-body">
        <h3>Search : <input v-model="search" type="text" placeholder="Search by Destination" /></h3> <hr>
          <div v-for="(n,index) in filterNodeConnect" :key="index">
            <h3>From: {{n.A}} - To: {{n.B}} - Type: {{n.status}} || <button class="btn btn-danger" @click="deleteNodeConn(n)">Delete</button> </h3>
          </div>
      </div>
    </div>
    <hr>
    <!-- #######################################Node Path############################################### -->
    <h2>Node Path Management</h2>
    <p>
      <button class="btn btn-primary" type="button" data-toggle="collapse" data-target="#addnodepath" aria-expanded="false" aria-controls="collapseExample" @click="getNullNodePath()">
          Add Path
      </button>
      <button class="btn btn-warning" type="button" data-toggle="collapse" data-target="#editnodepath" aria-expanded="false" aria-controls="collapseExample" @click="getNodePath()">
          Modify Path
      </button>
      <button class="btn btn-danger" type="button" data-toggle="collapse" data-target="#deletenodepath" aria-expanded="false" aria-controls="collapseExample" @click="getNodePath()">
          Delete Path
      </button>
    </p>
    <div class="collapse" id="addnodepath">
      <div class="card card-body">
          <h3>Search : <input v-model="search" type="text" placeholder="Search by Destination" /></h3> <hr>
          <div v-for="path in filterNodePath" :key="path.index">
              <h3>From: {{path.A}} - To: {{path.B}} - Type: {{path.status}} || <button class="btn btn-primary" @click="gotoAddNodePath(path)">Add</button></h3>
          </div>
      </div>
    </div>
    <div class="collapse" id="editnodepath">
      <div class="card card-body">
        <h3>Search : <input v-model="search" type="text" placeholder="Search by Destination" /></h3> <hr>
          <div v-for="path in filterNodePath" :key="path.index">
              <h3>From: {{path.A}} - To: {{path.B}} - Type: {{path.status}} || <button class="btn btn-warning" @click="gotoEditNodePath(path)">Edit</button></h3>
          </div>
      </div>
    </div>
    <div class="collapse" id="deletenodepath">
      <div class="card card-body">
        <h3>Search : <input v-model="search" type="text" placeholder="Search by Destination" /></h3> <hr>
          <div v-for="path in filterNodePath" :key="path.index">
              <h3>From: {{path.A}} - To: {{path.B}} - Type: {{path.status}} || <button class="btn btn-danger" @click="deleteNodePath(path)">Delete</button></h3>
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
      node: [],
      nodeConn: [],
      nodePath: [],
      search: ''
    }
  },
  methods: {
    gotoAddSwitch () {                                       // go to add switch page
      this.$router.push({name: 'AddSwitch'})
    },
    gotoModifySwitch (data) {                                       // go to edit switch page
      this.$router.push({name: 'EditSwitch', params: data})
    },
    gotoAddPath (data) {                                       // go to add path page
      this.$router.push({name: 'AddPath', params: data})
    },
    gotoEditPath (data) {                                       // go to edit path page
      this.$router.push({name: 'EditPath',params:data})
    },
    gotoAddUser () {                                       // go to add user page
      this.$router.push({name: 'AddUser'})
    },
    gotoEditUser (data) {                                       // go to edit user page
      this.$router.push({name: 'EditUser', params:data})
    },
    gotoChangePass(data) {                                       // go to change password page
      this.$router.push({name: 'ChangePass', params:data})
    },
    gotoAddNode () {                                       // go to add node page
      this.$router.push({name: 'AddNode'})
    },
    gotoEditNode (data) {                                       // go to edit node page
      this.$router.push({name: 'EditNode', params: data})
    },
    gotoAddNodeConnect () {                                       // go to add node connect page
      this.$router.push({name: 'AddNodeConnect'})
    },
    gotoAddNodePath (data) {                                       // go to add node path page
      this.$router.push({name: 'AddNodePath', params: data})
    },
    gotoEditNodePath (data) {                                       // go to edit node path page
      this.$router.push({name: 'EditNodePath', params: data})
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

    getSwitch () {                                       // Get switch from DB
      this.switchs = []
      this.axios
        .get('https://fibermap-api.cmu.ac.th/getswitch', {
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
        .then(response => {
          // console.log(response.data[0].name)
          this.switchs = response.data
        })
    },
    // deleteSwitch (data) {
    //   window.confirm('คุณต้องการลบ : ' + data + ' ?')
    // //   function delete switch
    // },
    getIp () {                                       // Get ip from DB
      this.ips = []
      this.getSwitch()
      this.axios.get('https://fibermap-api.cmu.ac.th/getip', {
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
        .then(response => {
        //   console.log(response.data[0].name)
          this.ips = response.data
          for(let i=0; i<this.ips.length; i++) {
            for(let j=0; j<this.switchs.length; j++) {
              if(this.ips[i].ip == this.switchs[j]['ip']) {
                this.ips[i].name = this.switchs[j].name
              }
              else if(this.ips[i].name == null) {
                this.ips[i].name = 'Not Register.'
              }
            }
          }
          // console.log(this.switchs[0]['ip'])
          // console.log(this.ips[0].ip)
        })
    },
    deleteIp (data) {                                       // Delete ip
      if (confirm('Are you delete IP : ' + data + ' ?') === true) {
        this.axios
          .get('https://fibermap-api.cmu.ac.th/deleteip', {
            params: {
              ip: data
            },
            headers: {'Authorization': sessionStorage.getItem('token')}
          })
          .then(response => {
            alert('Deleted IP success.')
            location.reload()
          })
      } else {
        console.log('no')
      }
    },
    getNullPath () {                                       // Get path without polyline
      this.paths = []
      this.axios
        .get('https://fibermap-api.cmu.ac.th/getrealpath', {
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
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
    getPath () {                                       // Get path with polyline
      this.paths = []
      this.axios
        .get('https://fibermap-api.cmu.ac.th/getrealpath', {
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
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
    deletePath (data) {                                       // Delete path
      if (confirm('Are you delete path : From ' + data.A + " To " + data.B + ' ?') === true) {
        this.axios
          .get('https://fibermap-api.cmu.ac.th/deletepath', {
            params: {
              line_id: data.id
            },
            headers: {'Authorization': sessionStorage.getItem('token')}
          })
          .then(response => {
            alert('Deleted path success.')
            location.reload()
          })
      } else {
        console.log('no')
      }
    },
    getUser (event) {                                       // Get User from DB
      this.infouser = []
      this.axios.get('https://fibermap-api.cmu.ac.th/getuser', {
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
      .then(response => {
        // console.log(event)
        // console.log(response.data)
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
    deleteUser (data) {                                       // Delete User
      if (confirm('Are you delete user : ' + data.firstname + "  " + data.lastname + ' ?') === true) {
        this.axios
          .get('https://fibermap-api.cmu.ac.th/deleteuser', {
            params: {
              user_id: data.id
            },
            headers: {'Authorization': sessionStorage.getItem('token')}
          })
          .then(response => {
            alert('Deleted user success.')
            location.reload()
          })
      } else {
        console.log('no')
      }
    },
    getNode () {                                       // Get node from DB
      this.node = []
        this.axios
          .get('https://fibermap-api.cmu.ac.th/getnode', {
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
          .then(response => {
            // console.log(response.data[0].name)
            this.node = response.data
        })
    },
    deleteNode (data) {                                       // Delete node
      if (confirm('Are you delete node : ' + data.name + ' ?') === true) {
        this.axios
          .get('https://fibermap-api.cmu.ac.th/deletenode', {
            params: {
              id: data.id
            },
            headers: {'Authorization': sessionStorage.getItem('token')}
          })
          .then(response => {
            alert('Deleted node success.')
            location.reload()
          })
      } else {
        console.log('no')
      }
    },
    getNodeConn () {                                       // Get node connection from DB
      this.node = []
        this.axios
          .get('https://fibermap-api.cmu.ac.th/getnodeconn', {
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
          .then(response => {
            // console.log(response.data[0].name)
            this.nodeConn = response.data
        })
    },
    deleteNodeConn (data) {                                       // Delete node connection
      if (confirm('Are you delete node connection : ' + data.A + " - " + data.B + " - " + data.status + ' ?') === true) {
        this.axios
          .get('https://fibermap-api.cmu.ac.th/deletenodeconn', {
            params: {
              id: data.id
            },
            headers: {'Authorization': sessionStorage.getItem('token')}
          })
          .then(response => {
            alert('Deleted node connection success.')
            location.reload()
          })
      } else {
        console.log('no')
      }
    },
    getNullNodePath () {                                       // Get node path without polyline
      this.nodePath = []
      this.axios
        .get('https://fibermap-api.cmu.ac.th/getnodepath', {
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
        .then(response => {
          this.nodePath = []
          for (let i = 0; i < response.data.length; i++) {
            if (response.data[i].path.length === 0) {
              this.nodePath.push(response.data[i])
            }
          }
        })
    },
    getNodePath () {                                       // Get node path with polyline
      this.nodePath = []
      this.axios
        .get('https://fibermap-api.cmu.ac.th/getnodepath', {
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
        .then(response => {
          this.nodePath = []
          for (let i = 0; i < response.data.length; i++) {
            if (response.data[i].path.length !== 0) {
              this.nodePath.push(response.data[i])
            }
          }
        })
    },
    deleteNodePath (data) {                                       // Delete node path
      if (confirm('Are you delete node path : ' + data.A + " - " + data.B + " - " + data.status + ' ?') === true) {
        this.axios
          .get('https://fibermap-api.cmu.ac.th/deletenodepath', {
            params: {
              line_id: data.id
            },
            headers: {'Authorization': sessionStorage.getItem('token')}
          })
          .then(response => {
            alert('Deleted node path success.')
            location.reload()
          })
      } else {
        console.log('no')
      }
    }
  },

  created () {                                       // Run these function when start page
    this.getDataUser()
    if (this.user.isAdmin !== true) {
      this.$router.push({name: 'Dashboard'})
    }
  },
  computed: {    // Filter data in each search box (Calculate only function not page)
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
    filterNode () {
      return this.node.filter(node => {
        return node.name.toLowerCase().match(this.search.toLowerCase())
      })
    },
    filterNodeConnect () {
      return this.nodeConn.filter(nodeConn => {
        return nodeConn.B.toLowerCase().match(this.search.toLowerCase())
      })
    },
    filterNodePath () {
      return this.nodePath.filter(nodePath => {
        return nodePath.B.toLowerCase().match(this.search.toLowerCase())
      })
    },
  }
}
</script>
