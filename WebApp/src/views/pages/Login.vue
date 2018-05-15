<template>
  <div class="app flex-row align-items-center">
    <div class="container">
      <b-row class="justify-content-center">
        <b-col md="8">
          <b-card-group>
            <b-card no-body class="p-4">
              <b-card-body>
                <h1>Login</h1>
                <p class="text-muted">Sign In to your account</p>
                <div class="input-group mb-3">
                  <span class="input-group-addon"><i class="icon-user"></i></span>
                  <input type="text" class="form-control" placeholder="Username" v-model="username" @keyup="keypressLogin">
                </div>
                <div class="input-group mb-4">
                  <span class="input-group-addon"><i class="icon-lock"></i></span>
                  <input type="password" class="form-control" placeholder="Password" v-model="password" @keyup="keypressLogin">
                </div>
                <b-row>
                  <b-col cols="6">
                    <b-button variant="primary" class="px-4" @click="isLogin()">Login</b-button>
                  </b-col>
                  <b-col cols="6" class="text-right">
                    <b-button variant="link" class="px-0" @click="toBack()"><h4>Back to Dashboard</h4></b-button>
                  </b-col>
                </b-row>
              </b-card-body>
            </b-card>
            <!-- <b-card no-body class="text-white bg-primary py-5 d-md-down-none" style="width:44%">
              <b-card-body class="text-center">
                <div>
                  <h2>Sign up</h2>
                  <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                  <b-button variant="primary" class="active mt-3">Register Now!</b-button>
                </div>
              </b-card-body>
            </b-card> -->
          </b-card-group>
        </b-col>
      </b-row>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data () {
    return {
      adminid: 'admin',
      adminpass: '123123123',
      username: '',
      password: ''
    }
  },
  methods: {
    isLogin () {
      this.axios.post('https://fibermap.herokuapp.com/authuser', {
        user: this.username,
        pass: this.password
      })
        .then(function (response) {
          if (response.data.length === 0) {
            window.alert('Invalid username & password')
          } else {
            let user = response.data
            sessionStorage.setItem('iduser', user[0].id)
            sessionStorage.setItem('username', user[0].username)
            sessionStorage.setItem('firstname', user[0].firstname)
            sessionStorage.setItem('lastname', user[0].lastname)
            sessionStorage.setItem('tel', user[0].tel)
            sessionStorage.setItem('email', user[0].email)
            sessionStorage.setItem('isAdmin', user[0].isAdmin)
            sessionStorage.setItem('isLogin', true)
            // this.$router.push({name: sessionStorage.getItem('prevPage')})
            // this.$router.push({name: 'Dashboard'})
            this.$router.push({name: 'RealPath'})
          }
        }.bind(this))
    },
    toBack () {
      this.$router.push({name: 'Dashboard'})
    },
    // isLogin1 () {
    //   if (this.username !== this.adminid || this.password !== this.adminpass) {
    //     window.alert('Invalid username & password')
    //   } else {
    //     sessionStorage.setItem('isAdmin', true)
    //     this.$router.push({name: sessionStorage.getItem('prevPage')})
    //   }
    // },
    keypressLogin (e) {
      // console.log(e.key)
      if (e.key === 'Enter') {
        this.isLogin()
      }
    }
  }
}
</script>
