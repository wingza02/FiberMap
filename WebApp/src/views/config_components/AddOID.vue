<template>
  <div>
    <div class="container">
      <div class="form-horizontal" role="form">
        <form @submit.prevent="onSubmit()">
          <div class="form-group" :class="{error: errors.has('Model')}">
              <label for="Model" class="col-sm-3 control-label">Model Switch</label>
              <div class="col-sm-9">
                  <select name="Model" id="Model" class="form-control" v-model="oid.model" v-validate="'required'">
                      <option v-for="m in models">{{m.id}}.{{m.model}}</option>
                  </select>
                  <span style="color:red" v-show="errors.has('Model')" class="alert alert-danger">{{ errors.first('Model') }}</span>
              </div>
          </div>  
          <div class="form-group" :class="{error: errors.has('Description')}">
              <label for="Description" class="col-sm-3 control-label">Description OID</label>
              <div class="col-sm-9">
                  <select name="Description" id="Description" class="form-control" v-model="oid.descript" v-validate="'required'">
                      <option v-for="d in descripts">{{d.id}}.{{d.descript}}</option>
                  </select>
                  <span style="color:red" v-show="errors.has('Description')" class="alert alert-danger">{{ errors.first('Description') }}</span>
              </div>
          </div>

          <div class="form-group" :class="{error: errors.has('OID')}">
              <label for="OID" class="col-sm-3 control-label">OID</label>
              <div class="col-sm-9">
                <input name="OID" id="OID" type="text" placeholder="OID" class="form-control" v-model="oid.oid" v-validate="'required'" />
                <span style="color:red" v-show="errors.has('OID')" class="alert alert-danger">{{ errors.first('OID') }}</span>
              </div>
          </div>
          <div class="form-group" :class="{error: errors.has('Slot')}">
              <label for="Slot" class="col-sm-3 control-label">Slot</label>
              <div class="col-sm-9">
                <input name="Slot" id="Slot" type="text" placeholder="Slot" class="form-control" v-model="oid.slot" v-validate="'required|numeric'" />
                <span style="color:red" v-show="errors.has('Slot')" class="alert alert-danger">{{ errors.first('Slot') }}</span>
              </div>
          </div>
          <div class="form-group">
              <div class="col-sm-9 col-sm-offset-3">
                  <button type="submit" class="btn btn-primary btn-block">Add OID</button>
              </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      user: [],
      models: [],
      descripts: [],
      oid:[]
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
    sendData () {                                       // send data to DB
      this.axios.get('https://fibermap-api.cmu.ac.th/addoid', {
          params: {
              model: this.oid.model.split('.')[0],
              descript: this.oid.descript.split('.')[0],
              oid: this.oid.oid,
              slot: this.oid.slot
          },
          headers: {'Authorization': sessionStorage.getItem('token')}
      })
      .then(function (response) {
        console.log(response.data)
        alert('Added oid success.')
        this.$router.push({name: 'Config'})
      }.bind(this))
    },
    goBack () {                                       // go back to config page
      this.$router.push({name: 'Config'})
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
    getModel () {                                       // Get Model from DB
      this.node = []
        this.axios
          .get('https://fibermap-api.cmu.ac.th/getmodel', {
            headers: {'Authorization': sessionStorage.getItem('token')}
          })
          .then(response => {
            // console.log(response.data[0].name)
            this.models = response.data
        })
    },
    getDescript () {                                       // Get descript from DB
      this.node = []
        this.axios
          .get('https://fibermap-api.cmu.ac.th/getdescript', {
            headers: {'Authorization': sessionStorage.getItem('token')}
          })
          .then(response => {
            // console.log(response.data[0].name)
            this.descripts = response.data
        })
    },
  },
  created () {                                       // Run these function when start page
    this.getDataUser()
    if (this.user.isAdmin !== true) {
      this.$router.push({name: 'Dashboard'})
    }
    this.getModel()
    this.getDescript()
  }
}
</script>

<style>
body {
    background-color: #eee;
}

*[role="form"] {
    max-width: 530px;
    padding: 15px;
    margin: 0 auto;
    background-color: #fff;
    border-radius: 0.3em;
}

*[role="form"] h2 {
    margin-left: 5em;
    margin-bottom: 1em;
}
</style>
