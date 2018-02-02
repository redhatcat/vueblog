<template>
  <div>
    <div v-if="!hasNoUsers" class="user-login">
      <b-form v-on:submit.prevent @submit="submit">
        <b-form-group>
          <b-form-input
            type="text"
            v-model="username"
            placeholder="username"/>
        </b-form-group>
        <b-form-group>
          <b-form-input
            type="password"
            v-model="password"
            placeholder="password"/>
        </b-form-group>
        <b-alert
          :show="error.length > 0"
          variant="danger">{{ error }}</b-alert>
        <button type="submit" class="btn btn-primary">login</button>
      </b-form>
    </div>
    <user-create
      v-if="hasNoUsers"
      :set-has-no-users="setHasNoUsers"
      :login-callback="login"
      :no-users="true"/>
  </div>
</template>

<script>
import axios from 'axios'
import UserCreate from '@/components/UserCreate'
import settings from '@/settings'

export default {
  name: 'UserLogin',
  computed: {
    error () { return this.$store.state.UserLogin.error }
  },
  components: { UserCreate },
  created () {
    this.checkUsers()
  },
  data () {
    return {
      username: '',
      password: '',
      confirmPassword: '',
      hasNoUsers: false,
      hasInvalidInputs: true
    }
  },
  methods: {
    checkUsers () {
      let comp = this
      axios.post(settings.apiUrl + '/api/users/empty')
        .then(function (response) {
          comp.setHasNoUsers(response.data.result)
        })
    },
    setHasNoUsers (value) {
      this.hasNoUsers = value
    },
    login (creds) {
      this.$store.dispatch('loginUser', creds)
    },
    submit () {
      this.login({
        username: this.username,
        password: this.password
      })
    }
  }
}
</script>

<style>
.user-login {
  padding: 10px;
}
</style>
