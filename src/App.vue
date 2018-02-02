<template>
  <div class="app">
    <AppHeader/>
    <div class="app-body">
      <Sidebar :navItems="nav"/>
      <main class="main">
        <breadcrumb :list="list"/>
        <div class="container-fluid">
          <router-view></router-view>
        </div>
      </main>
      <AppAside/>
    </div>
  </div>
</template>

<script>
import { Header as AppHeader, Sidebar, Aside as AppAside, Footer as AppFooter, Breadcrumb } from '@/components/'

const navItems = [
  {
    name: 'Home',
    url: '/',
    icon: 'icon-home'
  },
  {
    name: 'About Me',
    url: '/read/about-me',
    icon: 'icon-info'
  }
]

const loginItem = {
  name: 'Login',
  url: '/login',
  icon: 'icon-login'
}

const userItems = [
  {
    name: 'Write',
    icon: 'icon-pencil',
    url: '/write'
  },
  {
    name: 'Logout',
    icon: 'icon-logout',
    action: 'logoutUser'
  }
]

export default {
  name: 'app',
  components: {
    AppHeader,
    Sidebar,
    AppAside,
    AppFooter,
    Breadcrumb
  },
  computed: {
    nav () {
      let items = navItems.slice()
      if (this.username) {
        items = items.concat(userItems)
      } else {
        items.push(loginItem)
      }
      return items
    },
    name () {
      return this.$route.name
    },
    list () {
      return this.$route.matched
    },
    username () { return this.$store.state.user.username }
  },
  methods: {
    logout () {
      this.$store.dispatch('logoutUser')
    }
  }
}
</script>

<style lang="scss">
  // Import Main styles for this application
  @import './scss/style';
</style>
