<template>
  <div>
    <div class="container">
      <div class="form-horizontal" role="form">
        <form @submit.prevent="onSubmit()">
          <div class="form-group" :class="{error: errors.has('From')}">
              <label for="From" class="col-sm-3 control-label">From</label>
              <div class="col-sm-9">
                  <select name="From" id="From" class="form-control" v-model="node.A" v-validate="'required'" @click="minusA()">
                      <option v-for="n in nodes">{{n.id}}.{{n.name}}</option>
                  </select>
                  <span style="color:red" v-show="errors.has('From')" class="alert alert-danger">{{ errors.first('From') }}</span>
              </div>
          </div>  
          <div class="form-group" :class="{error: errors.has('To')}">
              <label for="To" class="col-sm-3 control-label">To</label>
              <div class="col-sm-9">
                  <select name="To" id="To" class="form-control" v-model="node.B" v-validate="'required'">
                      <option v-for="n in nodes2">{{n.id}}.{{n.name}}</option>
                  </select>
                  <span style="color:red" v-show="errors.has('To')" class="alert alert-danger">{{ errors.first('To') }}</span>
              </div>
          </div>

          <div class="form-group" :class="{error: errors.has('TypeLine')}">
              <label for="To" class="col-sm-3 control-label">Type Line</label>
              <div class="col-sm-9">
                  <select name="TypeLine" id="TypeLine" class="form-control" v-model="node.typeline" v-validate="'required'">
                      <option value="1">Main Path</option>
                      <option value="0">Simulate Path</option>
                  </select>
                  <span style="color:red" v-show="errors.has('TypeLine')" class="alert alert-danger">{{ errors.first('TypeLine') }}</span>
              </div>
          </div>
          <div class="form-group">
              <div class="col-sm-9 col-sm-offset-3">
                  <button type="submit" class="btn btn-primary btn-block">Add Node Connection</button>
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
      nodes: [],
      nodes2: [],
      node: [],
      user: []
    }
  },
  methods: {
    minusA() {                                       // node input B - input A
      this.nodes2 = []
      for(let i=0; i<this.nodes.length; i++) {
          if(this.node.A.split('.')[0] != this.nodes[i].id) {
              this.nodes2.push(this.nodes[i])
          }
      }
    },
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
      this.axios.get('https://fibermap-api.cmu.ac.th/addnodeconn', {
          params: {
              A: this.node.A.split('.')[0],
              B: this.node.B.split('.')[0],
              status: this.node.typeline
          },
          headers: {'Authorization': sessionStorage.getItem('token')}
      })
      .then(function (response) {
        console.log(response.data)
        alert('Added node connection success.')
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
    getNode () {                                       // Get node from DB
      this.node = []
        this.axios
          .get('https://fibermap-api.cmu.ac.th/getnode', {
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
          .then(response => {
            // console.log(response.data[0].name)
            this.nodes = response.data
        })
    },
  },
  created () {                                       // Run these function when start page
    this.getDataUser()
    if (this.user.isAdmin !== true) {
      this.$router.push({name: 'Dashboard'})
    }
    this.getNode()
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
