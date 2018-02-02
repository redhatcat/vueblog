<template>
  <div class="" v-bind:class="{ standalone: standalone }">
    <b-card v-if="post">
      <div slot="header">
        <router-link
          v-if="post.slug"
          :to="{ name: 'PostReader', params: { slug: post.slug } }">
          {{ post.title }}
        </router-link>
        <div
          v-if="canEdit"
          class="float-right">
          <router-link
            :to="{ name: 'PostWriter', params: { id: post.id } }">
            <i class="fa fa-pencil" aria-hidden="true"></i>
          </router-link>
          <a href="javascript:;"
            v-b-modal.deletePostModal>
            <i class="fa fa-trash" aria-hidden="true"></i>
          </a>
          <b-modal
            id="deletePostModal"
            @ok="trash"
            title="Deleting post...">
            Are you sure?
          </b-modal>
        </div>
      </div>
      <vue-markdown :source="post.body" :html="false"/>
      <div
        v-if="post.author"
        class="post-reader-meta">
        <div>
          Written by {{ post.author }}
          <timeago
            :since="post.published_at || post.created_at"
            :auto-update="60"/>
        </div>
        <div>
          Tags:
          <router-link
            v-for="tag in post.tags"
            :key="tag"
            :to="{name: 'PostListByTags', params:{tags: tag}}">
            {{ tag }}
          </router-link>
        </div>
      </div>
    </b-card>
    <div v-if="!post">
      <loader msg="Fetching post data"/>
    </div>
  </div>
</template>

<script>
import settings from '@/settings'
import VueMarkdown from 'vue-markdown'
import Loader from '@/components/Loader'
import axios from 'axios'
import Prism from 'prismjs/prism.js'

export default {
  name: 'PostReader',
  props: [ 'item' ],
  data () {
    return {
      dataPost: undefined
    }
  },
  computed: {
    canEdit () {
      return this.$store.state.user.username && this.post.id && this.standalone
    },
    standalone () {
      return !!this.$route.params.slug
    },
    post: {
      get () {
        return this.dataPost || this.item
      },
      set (newValue) {
        this.dataPost = newValue
        this.onPostUpdate(newValue)
      }
    }
  },
  components: { Loader, VueMarkdown },
  created () {
    this.onCreate()
  },
  watch: {
    '$route': 'onCreate',
    dataPost: 'onPostUpdate'
  },
  methods: {
    onCreate () {
      if (this.$route.params.slug) {
        let comp = this
        let data = {}
        data.slug = this.$route.params.slug
        axios.post(settings.apiUrl + '/api/posts', data)
          .then(function (response) {
            comp.post = response.data.items[0]
            document.title = comp.post.title + ' - ' + settings.branding
          })
          .catch(function (error) {
            console.log(error)
          })
      } else {
        this.onPostUpdate()
      }
    },
    onPostUpdate () {
      setTimeout(() => {
        Prism.highlightAll()
      }, 100)
    },
    trash () {
      let comp = this
      let data = {}
      data.id = this.post.id
      axios.post(settings.apiUrl + '/api/posts/delete', data)
        .then(function (response) {
          response.data.trash = true
          comp.$store.dispatch('updateBlogItem', response.data)
          comp.$router.push('/')
        })
        .catch(function (error) {
          console.log(error)
        })
    }
  }
}
</script>

<style>
.post-reader {
  padding: 10px;
  border: 1px solid #acbed0;
  border-radius: 5px;
}
.post-reader.standalone {
  margin: 10px;
}
.post-reader-meta {
  text-align: right;
  font-size: .75em;
}

.post-reader pre {
  border-radius: 5px;
  margin-bottom: 12px;
}
</style>
