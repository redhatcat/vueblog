<template>
  <ol class="breadcrumb">
    <li class="breadcrumb-item" v-for="(item, index) in list">
      <span class="active" v-if="isLast(index)">{{ showName(item) }}</span>
      <router-link :to="item" v-else>{{ showName(item) }}</router-link>
      <b-nav-form
        v-if="isPostList"
        class="post-tag-filter"
        v-on:submit.prevent
        @submit="filterByTags">
        <b-form-input
          v-model='tagstring'
          size="sm"
          class="mr-sm-2"
          type="text"
          placeholder="filter by tags"/>
      </b-nav-form>
    </li>
  </ol>
</template>

<script>
export default {
  props: {
    list: {
      type: Array,
      required: true,
      default: () => []
    }
  },
  created () {
    this.updateTags()
  },
  computed: {
    isPostList () {
      return this.$route.name === 'PostList' ||
        this.$route.name === 'PostListByTags'
    }
  },
  data () {
    return {
      tagstring: ''
    }
  },
  watch: {
    '$store.state.blog.tags': 'updateTags'
  },
  methods: {
    filterByTags () {
      this.$router.push({
        name: 'PostListByTags',
        params: {tags: this.tagstring.split(' ').join(',')}
      })
    },
    isLast (index) {
      return index === this.list.length - 1
    },
    showName (item) {
      if (item.meta && item.meta.label) {
        item = item.meta && item.meta.label
      }
      if (item.name) {
        item = item.name
      }
      return item
    },
    updateTags () {
      let tags = this.$store.state.blog.tags || ''
      this.tagstring = tags.split(',').join(' ')
    }
  }
}
</script>

<style>
.post-tag-filter {
  display: inline-block;
}
</style>
