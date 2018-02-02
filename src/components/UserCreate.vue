<template>
  <div class="user-create">
    <h1 v-if="noUsers">create the first user</h1>
    <b-form v-on:submit.prevent @submit="submit" @input="checkValid">
      <b-form-group>
        <b-form-input
          type="text"
          v-model="username"
          placeholder="username made of letters, numbers, underscores, and/or dashes"/>
      </b-form-group>
      <b-form-group>
        <b-form-input
          type="password"
          v-model="password"
          placeholder="a password"/>
      </b-form-group>
      <b-form-group>
        <b-form-input
          type="password"
          v-model="confirmPassword"
          placeholder="that same password again"/>
      </b-form-group>
      <b-button
        variant="primary"
        type="submit"
        v-bind:disabled="hasInvalidInputs">
        create user
        <span v-if=loginCallback>&amp; log in</span>
      </b-button>
    </b-form>
  </div>
</template>

<script>
import axios from 'axios'
import settings from '@/settings'

export default {
  name: 'UserCreate',
  props: [ 'noUsers', 'loginCallback', 'setHasNoUsers' ],
  data () {
    return {
      username: '',
      password: '',
      confirmPassword: '',
      hasInvalidInputs: true
    }
  },
  created () {
  },
  methods: {
    checkValid () {
      this.hasInvalidInputs = false
    },
    submit () {
      let comp = this
      axios.post(settings.apiUrl + '/api/users/create', {
        username: this.username,
        password: this.password
      }).then(function (response) {
        if (comp.noUsers && comp.setHasNoUsers) {
          comp.setHasNoUsers(true)
        }
        if (comp.loginCallback) {
          comp.loginCallback({
            username: comp.username,
            password: comp.password
          })
        }
      })
    }
  }
}
</script>

<style>
.user-create {
  padding: 10px;
}
</style>
