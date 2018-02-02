import axios from 'axios'
import router from '../router'
import store from '../store'
import settings from '@/settings'

export const clearRenewInterval = ({commit}) => {
  clearInterval(store.state.user.interval)
  commit('setUserInterval', undefined)
}

export const updateBlogItem = ({ commit }, item, trash) => {
  commit('updateBlogItem', item)
}

export const fetchOlderBlogItems = ({ commit }) => {
  commit('setBlogLoading', true)
  let data = {}
  if (store.state.blog.items.length > 0) {
    data['after'] = store.state.blog.items[store.state.blog.items.length - 1]['id']
  }
  if (store.state.blog.tags) {
    data['tags'] = store.state.blog.tags.split(',')
  }
  axios.post(settings.apiUrl + '/api/posts', data)
    .then(function (response) {
      if (response.data.items.length < 1) {
        commit('setBlogFetchComplete', true)
      } else {
        commit('addBlogItems', response.data.items)
      }
      commit('setBlogLoading', false)
    })
    .catch(function (error) {
      console.log(error)
    })
}

export const fetchNewerBlogItems = ({ commit, dispatch }) => {
  let data = {}
  if (store.state.blog.items.length < 1) {
    return
  }
  data['since'] = store.state.blog.items[0]['id']
  axios.post(settings.apiUrl + '/api/posts', data)
    .then(function (response) {
      if (response.data.items.length > 0) {
        commit('prependBlogItems', response.data.items)
        dispatch('fetchNewerBlogItems')
      }
    })
    .catch(function (error) {
      console.log(error)
    })
}

export const renewAuthToken = ({commit}) => {
  let token = store.state.user.token
  if (!token) {
    return
  }
  axios.post(settings.apiUrl + '/api/users/renew')
    .then(function (response) {
      commit('setUserData', response.data)
      store.dispatch('setAuthToken')
    })
    .catch(function (error) {
      store.dispatch('logoutUser', error)
    })
}

export const setAuthToken = ({ commit }) => {
  let token = store.state.user.token
  axios.defaults.headers.common['Authorization'] = 'Bearer ' + token
  store.dispatch('setRenewInterval')
}

export const setRenewInterval = ({commit}) => {
  if (store.state.user.interval) {
    return
  }
  let token = store.state.user.token
  if (token) {
    let interval = setInterval(function () {
      store.dispatch('renewAuthToken')
    }, 10 * 60 * 1000) // 10 minutes
    commit('setUserInterval', interval)
  }
}

export const loginUser = ({ commit }, creds) => {
  axios.post(settings.apiUrl + '/api/users/login', {
    username: creds.username,
    password: creds.password
  })
    .then(function (response) {
      commit('setUserData', response.data)
      store.dispatch('setAuthToken')
      router.push('/')
    })
    .catch(function (error) {
      commit('setUserLoginError', error.response.data.msg)
    })
}

export const logoutUser = ({ commit }, reason) => {
  commit('setUserData', {'username': '', 'access_token': ''})
  store.dispatch('setAuthToken')
  store.dispatch('clearRenewInterval')
  router.push('/')
}

export const setTagFilter = ({ commit, dispatch }, tags) => {
  commit('setBlogFetchComplete', false)
  commit('clearBlogItems')
  commit('setTagFilter', tags)
}
