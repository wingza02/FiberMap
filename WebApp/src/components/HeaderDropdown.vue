<template>
  <div>
    <div v-show="isLogin==true" style="margin: 20px">
      <b-nav-item-dropdown right no-caret>
        <template slot="button-content">
          <!-- <img src="static/img/avatars/6.jpg" class="img-avatar" alt="admin@bootstrapmaster.com" > -->
          <h2>{{ firstname }} {{ lastname }}</h2>
        </template>
        <!-- <b-dropdown-header tag="div" class="text-center"><strong>Account</strong></b-dropdown-header>
        <b-dropdown-item><i class="fa fa-bell-o"></i> Updates<b-badge variant="info">{{itemsCount}}</b-badge></b-dropdown-item>
        <b-dropdown-item><i class="fa fa-envelope-o"></i> Messages<b-badge variant="success">{{itemsCount}}</b-badge></b-dropdown-item>
        <b-dropdown-item><i class="fa fa-tasks"></i> Tasks<b-badge variant="danger">{{itemsCount}}</b-badge></b-dropdown-item>
        <b-dropdown-item><i class="fa fa-comments"></i> Comments<b-badge variant="warning">{{itemsCount}}</b-badge></b-dropdown-item>
        <b-dropdown-header tag="div" class="text-center"><strong>Settings</strong></b-dropdown-header>
        <b-dropdown-item><i class="fa fa-user"></i> Profile</b-dropdown-item>
        <b-dropdown-item><i class="fa fa-wrench"></i> Settings</b-dropdown-item>
        <b-dropdown-item><i class="fa fa-usd"></i> Payments<b-badge variant="default">{{itemsCount}}</b-badge></b-dropdown-item>
        <b-dropdown-item><i class="fa fa-file"></i> Projects<b-badge variant="primary">{{itemsCount}}</b-badge></b-dropdown-item>
        <b-dropdown-divider></b-dropdown-divider>
        <b-dropdown-item><i class="fa fa-shield"></i> Lock Account</b-dropdown-item> -->
        <!-- <b-dropdown-item><i class="fa fa-lock" @click="isLogout()"></i> Logout</b-dropdown-item> -->
        <b-dropdown-item @click="isLogout()">Logout</b-dropdown-item>
      </b-nav-item-dropdown>
    </div>
    <div v-show="isLogin==false">
      <p @click="goLogin" style="margin: 20px">
        <img src="http://www.clker.com/cliparts/x/S/v/B/t/e/thin-gray-login-button-hi.png" alt="login-logo" style="width: 100px">
      </p>
    </div>
    <!-- <button @click="isLogout()">logout1!!</button>
    <button @click="status()">status user now</button> -->
  </div>
</template>
<script>
  export default {
    name: 'header-dropdown',
    data () {
      return {
        isLogin: sessionStorage.getItem('isLogin') === 'true',
        firstname: sessionStorage.getItem('firstname'),
        lastname: sessionStorage.getItem('lastname')
      }
    },
    methods: {
      status () {
        console.log(sessionStorage.getItem('isAdmin'))
      },
      goLogin () {
        sessionStorage.setItem('prevPage', this.$router.currentRoute.name)
        this.$router.push({name: 'Login'})
      },
      isLogout () {
        sessionStorage.removeItem('iduser')
        sessionStorage.removeItem('username')
        sessionStorage.removeItem('firstname')
        sessionStorage.removeItem('lastname')
        sessionStorage.removeItem('tel')
        sessionStorage.removeItem('email')
        sessionStorage.setItem('isAdmin', false)
        sessionStorage.setItem('isLogin', false)
        this.$router.go(this.$router.currentRoute)
      }
    },
    mounted: function () {
      if (sessionStorage.getItem('isAdmin') !== null) {
        this.isAdmin = sessionStorage.getItem('isAdmin') === 'true'
      } else {
        this.isAdmin = false === 'true'
      }
      // this.fisrtname = sessionStorage.getItem('firstname')
      // this.lastname = sessionStorage.getItem('lastname')
    }
  }
</script>

