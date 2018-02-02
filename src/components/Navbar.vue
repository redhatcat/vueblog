<template>
  <b-navbar toggleable="md" type="dark" variant="info">
    <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
    <b-navbar-brand :to="{ name: 'PostList' }">{{ settings.branding }}</b-navbar-brand>
    <b-collapse is-nav id="nav_collapse">
      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-nav-form
          v-on:submit.prevent
          @submit="filterByTags">
          <b-form-input
            v-model='tagstring'
            size="sm"
            class="mr-sm-2"
            type="text"
            placeholder="filter by tags"/>
        </b-nav-form>
        <b-nav-item v-if="username" :to="{ name: 'PostWriter' }">Write</b-nav-item>
        <b-nav-item v-if="username" @click="logout" href="javascript:;">@{{ username }}</b-nav-item>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
import settings from '@/settings'

export default {
  name: 'Navbar',
  data () {
    return {
      tagstring: ''
    }
  },
  created () {
    this.updateTags()
  },
  watch: {
    '$store.state.blog.tags': 'updateTags'
  },
  computed: {
    settings () { return settings },
    username () { return this.$store.state.user.username }
  },
  methods: {
    filterByTags () {
      this.$router.push({
        name: 'PostListByTags',
        params: {tags: this.tagstring.split(' ').join(',')}
      })
    },
    updateTags () {
      let tags = this.$store.state.blog.tags || ''
      this.tagstring = tags.split(',').join(' ')
    },
    logout () { this.$store.dispatch('logoutUser') }
  }
}
</script>

<style>
.user-login {
  padding: 10px;
}
</style>
