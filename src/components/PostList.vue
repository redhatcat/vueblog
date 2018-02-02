<template>
  <div class="post-list">
    <b-alert
      v-if="tags"
      variant="info"
      show>
      filtering by tags: {{ tags.split(',').join(' ') }}
      <router-link to="/">
        <i class="fa fa-times-circle" aria-hidden="true"></i>
      </router-link>
    </b-alert>
    <div v-for="item in items">
      <post-reader :item="item"/>
    </div>
    <loader v-if="loading" msg="Loading Blog Entries..."/>
    <b-container v-if="!loading">
      <b-row>
        <b-button
          v-if="!fetchComplete"
          variant="primary"
          class="col-md-12"
          @click="loadMore"
          v-observe-visibility="loadMoreButtonVisibilityChanged">
          load more
        </b-button>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import settings from '@/settings'
import PostReader from '@/components/PostReader'
import Loader from '@/components/Loader'

import Vue from 'vue'
import VueObserveVisibility from 'vue-observe-visibility'

Vue.use(VueObserveVisibility)

export default {
  name: 'PostList',
  components: { PostReader, Loader },
  computed: {
    items () { return this.$store.state.blog.items },
    loading () { return this.$store.state.blog.loading },
    fetchComplete () { return this.$store.state.blog.fetchComplete },
    tags () { return this.$store.state.blog.tags }
  },
  created () {
    this.onCreate()
  },
  watch: {
    '$route': 'onCreate'
  },
  methods: {
    onCreate () {
      document.title = settings.branding
      if (this.$route.params.tags) {
        document.title = 'posts with tags: ' + this.$route.params.tags + ' - ' + settings.branding
      }
      if (this.$route.params.tags !== this.$store.state.blog.tags) {
        this.$store.dispatch('setTagFilter', this.$route.params.tags)
      }
      if (this.items.length < 1) {
        this.loadMore()
      } else {
        this.checkNewPosts()
      }
    },
    checkNewPosts () {
      this.$store.dispatch('fetchNewerBlogItems')
    },
    loadMore () {
      this.$store.dispatch('fetchOlderBlogItems')
    },
    loadMoreButtonVisibilityChanged (isVisible, entry) {
      if (isVisible) {
        this.loadMore()
      }
    }
  }
}
</script>

<style>
</style>
