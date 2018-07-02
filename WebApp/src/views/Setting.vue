<template>
  <div>
<!-- ########################################## Model ############################################# -->
    <h2>Model Switch Management</h2>
    <p>
      <button class="btn btn-primary" type="button" data-toggle="collapse" data-target="#addModel" aria-expanded="false" aria-controls="collapseExample">
          Add Model
      </button>
      <button class="btn btn-danger" type="button" data-toggle="collapse" data-target="#deleteModel" aria-expanded="false" aria-controls="collapseExample" @click="getModel()">
          Manage IP Address
      </button>
    </p>
    <div class="collapse" id="addModel">
      <div class="card card-body">
        <h3>Model: <input type="text" v-model="model"/> || <button @click="addModel()">Add</button></h3>
      </div>
    </div>

    <div class="collapse" id="deleteModel">
      <div class="card card-body">
        <h3>Search : <input v-model="search" type="text" placeholder="Search by Model" /></h3> <hr>
          <div v-for="m in filterModel" :key="m.index">
              <h3>{{m.id}}. {{ m.model }} || <button class="btn btn-danger" @click="deleteModel(m)">Delete</button></h3>
          </div>
      </div>
    </div>
    <hr>
<!-- ######################################## OID Description ###################################### -->
    <h2>OID Description Management</h2>
    <p>
      <button class="btn btn-primary" type="button" data-toggle="collapse" data-target="#addDescript" aria-expanded="false" aria-controls="collapseExample">
          Add Description OID
      </button>
      <button class="btn btn-danger" type="button" data-toggle="collapse" data-target="#deleteDescript" aria-expanded="false" aria-controls="collapseExample" @click="getDescript()">
          Delete Description OID
      </button>
    </p>
    <div class="collapse" id="addDescript">
      <div class="card card-body">
        <h3>Description OID: <input type="text" v-model="descript_oid"/> || <button @click="addDescript()">Add</button></h3>
      </div>
    </div>

    <div class="collapse" id="deleteDescript">
      <div class="card card-body">
        <h3>Search : <input v-model="search" type="text" placeholder="Search by OID Description" /></h3> <hr>
          <div v-for="d in filterDescript" :key="d.index">
              <h3>{{d.id}}. {{ d.descript }} || <button class="btn btn-danger" @click="deleteDescript(d)">Delete</button></h3>
          </div>
      </div>
    </div>
    <hr>
<!-- ############################################ OID ############################################## -->
    <h2>OID Management</h2>
    <p>
      <button class="btn btn-primary" @click="gotoAddOID()">Add OID</button>
      <button class="btn btn-danger" type="button" data-toggle="collapse" data-target="#deleteoid" aria-expanded="false" aria-controls="collapseExample" @click="getOID()">
          Delete OID
      </button>
    </p>
    <div class="collapse" id="deleteoid">
      <div class="card card-body">
        <h3>Search : <input v-model="search" type="text" placeholder="Search by Model" /></h3> <hr>
          <div v-for="(oid,index) in filterOID" :key="index">
            <h3>{{oid.model}} - {{oid.oid}} - {{oid.descript}} || <button class="btn btn-danger" @click="deleteOID(oid)">Delete</button></h3>
          </div>
      </div>
    </div>
    <hr>
  </div>
</template>

<script>
export default {
  data () {
    return {
      user: [],
      model: '',
      models: [],
      descript_oid: '',
      descript_oids: [],
      oid: '',
      oids: [],
      search: ''
    }
  },
  methods: {
    gotoAddOID () {                                       // go to add OID page
      this.$router.push({name: 'AddOID'})
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

    getModel () {                                       // Get switch from DB
      this.axios
        .get('https://fibermap-api.cmu.ac.th/getmodel', {
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
        .then(response => {
          this.models = response.data
        })
    },
    addModel () {                                       // Add Model
      console.log(this.model)
      this.axios.get('https://fibermap-api.cmu.ac.th/addmodel', {
        params: {
          model: this.model
        },
        headers: {'Authorization': sessionStorage.getItem('token')}
      })
      .then(response => {
          window.alert('Added model switch success.')
          location.reload()
        })
    },
    deleteModel (data) {                                       // Delete Model
      if (confirm('Are you delete Model : ' + data.model + ' ?') === true) {
        this.axios
          .get('https://fibermap-api.cmu.ac.th/deletemodel', {
            params: {
              id: data.id
            },
            headers: {'Authorization': sessionStorage.getItem('token')}
          })
          .then(response => {
            alert('Deleted model switch success.')
            location.reload()
          })
      } else {
        console.log('no')
      }
    },

    getDescript () {                                       // Get Description OID from DB
      this.switchs = []
      this.axios
        .get('https://fibermap-api.cmu.ac.th/getdescript', {
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
        .then(response => {
          this.descript_oids = response.data
        })
    },
    addDescript () {                                       // Delete Description OID
      console.log(this.model)
      this.axios.get('https://fibermap-api.cmu.ac.th/adddescript', {
        params: {
          descript: this.descript_oid
        },
        headers: {'Authorization': sessionStorage.getItem('token')}
      })
      .then(response => {
          window.alert('Added oid description success.')
          location.reload()
        })
    },
    deleteDescript (data) {                                       // Delete Description OID
      if (confirm('Are you delete OID Description : ' + data.descript + ' ?') === true) {
        this.axios
          .get('https://fibermap-api.cmu.ac.th/deletedescript', {
            params: {
              id: data.id
            },
            headers: {'Authorization': sessionStorage.getItem('token')}
          })
          .then(response => {
            alert('Deleted oid description success.')
            location.reload()
          })
      } else {
        console.log('no')
      }
    },

    getOID () {                                       // Get OID from DB
      this.switchs = []
      this.axios
        .get('https://fibermap-api.cmu.ac.th/getoid', {
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
        .then(response => {
          this.oids = response.data
        })
    },
    deleteOID (data) {                                       // Delete OID
      if (confirm('Are you delete OID : ' + data.model + ' - ' + data.oid + ' ?') === true) {
        this.axios
          .get('https://fibermap-api.cmu.ac.th/deleteoid', {
            params: {
              id: data.id
            },
            headers: {'Authorization': sessionStorage.getItem('token')}
          })
          .then(response => {
            alert('Deleted oid success.')
            location.reload()
          })
      } else {
        console.log('no')
      }
    },
  },
  created () {                                       // Run these function when start page
    this.getDataUser()
    if (this.user.isAdmin !== true) {
      this.$router.push({name: 'Dashboard'})
    }
  },
  computed: {    // Filter data in each search box (Calculate only function not page)
    filterModel () {
      return this.models.filter(mo => {
        return mo.model.toLowerCase().match(this.search.toLowerCase())
      })
    },
    filterDescript () {
      return this.descript_oids.filter(des => {
        return des.descript.match(this.search.toLowerCase())
      })
    },
    filterOID () {
      return this.oids.filter(oid => {
        return oid.model.toLowerCase().match(this.search.toLowerCase())
      })
    },
  }
}
</script>
