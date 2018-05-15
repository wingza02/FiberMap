<template>
  <div>
    <div class="container">
      <div class="form-horizontal" role="form">
        <form @submit.prevent="onSubmit()">
          <div class="form-group" :class="{error: errors.has('Username')}">
              <label for="username" class="col-sm-3 control-label">Username</label>
              <div class="col-sm-9">
                <input name="Username" id="username" type="text" placeholder="Username" class="form-control" v-model="addUser.username" v-validate="'required|alpha_num'" autofocus />
                <span style="color:red" v-show="errors.has('Username')" class="alert alert-danger">{{ errors.first('Username') }}</span>
              </div>
          </div>
          <div class="form-group" :class="{error: errors.has('Password')}">
              <label for="password" class="col-sm-3 control-label">Password</label>
              <div class="col-sm-9">
                  <input name="Password" type="password" id="password" placeholder="Password" class="form-control" v-model="addUser.password" v-validate="'required|min:6|confirmed:cPassword'"/>
                  <span style="color:red" v-show="errors.has('Password')" class="alert alert-danger">{{ errors.first('Password') }}</span>
              </div>
              <label for="Cpassword" class="col-sm-3 control-label">Confirm Password</label>
              <div class="col-sm-9">
                  <input name="cPassword" type="password" id="Cpassword" placeholder="Confirm Password" class="form-control">
              </div>
          </div>
          <div class="form-group">
              <label for="firstName" class="col-sm-3 control-label">First Name</label>
              <div class="col-sm-9" :class="{error: errors.has('First Name')}">
                  <input name="First Name" type="text" id="firstName" placeholder="First Name" class="form-control" v-model="addUser.firstname" v-validate="'required|alpha'">
                  <span style="color:red" v-show="errors.has('First Name')" class="alert alert-danger">{{ errors.first('First Name') }}</span>
              </div>
              <label for="lastname" class="col-sm-3 control-label">Last Name</label>
              <div class="col-sm-9" :class="{error: errors.has('Last Name')}">
                  <input name="Last Name" type="text" id="lastName" placeholder="Last Name" class="form-control" v-model="addUser.lastname" v-validate="'required|alpha'">
                  <span style="color:red" v-show="errors.has('Last Name')" class="alert alert-danger">{{ errors.first('Last Name') }}</span>
              </div>
          </div>
          <div class="form-group" :class="{error: errors.has('Email')}">
              <label for="email" class="col-sm-3 control-label">Email</label>
              <div class="col-sm-9">
                <input type="text" name="Email" id="email" placeholder="Email" class="form-control" v-model="addUser.email" v-validate="'required|email'">
                <span style="color:red" v-show="errors.has('Email')" class="alert alert-danger">{{ errors.first('Email') }}</span>
              </div>
          </div>
          <div class="form-group" :class="{error: errors.has('Tel')}">
              <label for="tel" class="col-sm-3 control-label">Tel.</label>
              <div class="col-sm-9">
                  <input name="Tel" type="text" id="tel" class="form-control" placeholder="เบอร์โทรศัพท์" v-model="addUser.tel" v-validate="'required|numeric'">
                  <span style="color:red" v-show="errors.has('Tel')" class="alert alert-danger">{{ errors.first('Tel') }}</span>
              </div>
          </div>
          <div class="form-group" :class="{error: errors.has('Tel')}">
              <label for="country" class="col-sm-3 control-label">Role</label>
              <div class="col-sm-9">
                  <select name="Role" id="position" class="form-control" v-model="addUser.isAdmin" v-validate="'required'">
                      <option value="1">Admin</option>
                      <option value="0">Technician</option>
                  </select>
                  <span style="color:red" v-show="errors.has('Role')" class="alert alert-danger">{{ errors.first('Role') }}</span>
              </div>
          </div> <!-- /.form-group -->
          <div class="form-group">
              <div class="col-sm-9 col-sm-offset-3">
                  <button type="submit" class="btn btn-primary btn-block">Register</button>
              </div>
          </div>
        </form>
      </div>
    </div> <!-- ./container -->
  </div>
</template>

<script>
export default {
  data () {
    return {
      addUser: {
        username: null,
        password: null,
        firstname: null,
        lastname: null,
        email: null,
        tel: null,
        isAdmin: null
      },
      user: []
    }
  },
  methods: {
    onSubmit() {
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
    sendData () {
        // console.log('1')
      this.axios.post('https://fibermap.herokuapp.com/adduser', {
        username: this.addUser.username,
        password: this.addUser.password,
        firstname: this.addUser.firstname,
        lastname: this.addUser.lastname,
        tel: this.addUser.tel,
        email: this.addUser.email,
        isAdmin: this.addUser.isAdmin
      })
      .then(function (response) {
        console.log(response.data)
        alert('Added user success.')
        this.$router.push({name: 'Config'})
      }.bind(this))
    },
    goBack () {
      this.$router.push({name: 'Config'})
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
    }
  },
  created () {
    this.getDataUser()
    if (this.user.isAdmin !== true) {
      this.$router.push({name: 'Dashboard'})
    }
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
