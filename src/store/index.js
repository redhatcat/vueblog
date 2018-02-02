import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'

import * as actions from './actions'
import * as getters from './getters'
import * as mutations from './mutations'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: {
      username: '',
      token: '',
      interval: undefined
    },
    blog: {
      fetchComplete: false,
      tags: '',
      items: [],
      loading: false
    },
    UserLogin: {
      error: ''
    }
  },
  actions,
  getters,
  mutations,
  plugins: [createPersistedState({
    paths: ['user.username', 'user.token']
  })]
})
