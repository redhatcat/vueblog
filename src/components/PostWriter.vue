<template>
  <div class="post-writer">
    <b-form v-on:submit.prevent @submit="submit">
      <b-container fluid>
        <b-row>
          <b-col>
            <b-form-group>
              <label for="title">title</label>
              <b-form-input
                id="title"
                type="text"
                v-model="title"
                @input ="slug = slugify(title)"
                placeholder="title"/>
            </b-form-group>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <b-form-group>
              <label for="slug">slug</label>
              <b-form-input
                id="slug"
                type="text"
                v-model="slug"
                placeholder="slug"/>
            </b-form-group>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <b-form-group>
              <label for="body">body</label>
              <b-form-textarea
                id="body"
                v-model="body"
                :rows="5"
                :max-rows="20"
                placeholder="body"/>
            </b-form-group>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <b-form-group>
              <label for="tags">tags</label>
              <b-form-input
                id="tags"
                type="text"
                v-model="tags"
                placeholder="tags separated by spaces"/>
            </b-form-group>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <b-form-group>
              <label for="publishedAtDate">publish at date</label>
              <b-form-input
                id="publishedAtDate"
                type="date"
                v-model="publishedAtDate"
                placeholder="publish at this time"/>
            </b-form-group>
          </b-col>
          <b-col>
            <b-form-group>
              <label for="publishedAtTime">publish at time</label>
              <b-form-input
                id="publishedAtTime"
                type="time"
                v-model="publishedAtTime"
                placeholder="publish at this time"/>
            </b-form-group>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <b-form-group>
              <label for="author">author</label>
              <b-form-input
                id="author"
                type="text"
                v-model="author"
                placeholder="a pen name (will use your username by default)"/>
            </b-form-group>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <b-alert
              :show="showPublishAlert"
              dismissible
              @dismissed="showPublishAlert=false">
              Post has been saved!
            </b-alert>
            <b-alert
              :show="error.length > 0"
              dismissible
              @dismissed="error = ''"
              variant="danger">{{ error }}</b-alert>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <b-button
              variant="primary"
              type="submit">
              save
            </b-button>
            <b-button
              @click="$router.go(-1)">
              cancel
            </b-button>
          </b-col>
        </b-row>
      </b-container>
    </b-form>

    <div>preview:</div>
    <post-reader :item="item"/>
  </div>
</template>

<script>
import axios from 'axios'
import PostReader from '@/components/PostReader'
import settings from '@/settings'
import Prism from 'prismjs/prism.js'

function data () {
  return {
    id: '',
    title: '',
    slug: '',
    body: '',
    tags: '',
    publishedAtDate: '',
    publishedAtTime: '',
    author: '',
    error: '',
    showPublishAlert: false
  }
}

export default {
  name: 'PostWriter',
  components: { PostReader },
  data,
  computed: {
    item () {
      return {
        id: this.id,
        title: this.title,
        slug: this.slug,
        body: this.body,
        tags: this.tags.split(' '),
        published_at: new Date(`${this.publishedAtDate}T${this.publishedAtTime || '00:00:00'}`),
        author: this.author
      }
    }
  },
  created () {
    if (this.$route.params.id) {
      let comp = this
      let data = {}
      data.id = this.$route.params.id
      axios.post(settings.apiUrl + '/api/posts', data)
        .then(function (response) {
          let item = response.data.items[0]
          comp.id = item.id
          comp.title = item.title
          comp.slug = item.slug
          comp.body = item.body
          comp.tags = item.tags.join(' ')
          comp.author = item.author

          if (item.published_at) {
            // Adjust published_at for timezones
            let tzoffset = (new Date()).getTimezoneOffset() * 60000
            let publishedAtUTC = new Date(item.published_at)
            let publishedAt = (new Date(publishedAtUTC - tzoffset)).toISOString().slice(0, -1)
            comp.publishedAtDate = publishedAt.split('T')[0]
            comp.publishedAtTime = publishedAt.split('T')[1].substring(0, 8)
          }
        })
    }
  },
  watch: {
    body: 'onBodyUpdate'
  },
  methods: {
    onBodyUpdate () {
      setTimeout(() => {
        Prism.highlightAll()
      }, 100)
    },
    slugify (str) {
      return str.toLowerCase().replace(/\W+/g, '-')
    },
    reset () {
      Object.assign(this.$data, data())
    },
    submit () {
      let comp = this
      let item = Object.assign({}, this.item)
      let slug = item.slug
      item.published_at = item.published_at || null
      let url = settings.apiUrl + '/api/posts/create'
      if (comp.id) {
        url = settings.apiUrl + '/api/posts/update'
      }
      axios.post(url, item)
        .then(function (response) {
          comp.reset()
          comp.showPublishAlert = true
          comp.$router.push({name: 'PostReader', params: {slug: slug}})
          comp.$store.commit('updateBlogItem', response.data)
        })
        .catch(function (error) {
          if (error.response) {
            comp.error = error.response.data.msg
          } else {
            console.log(error)
            comp.error = 'an error occurred'
          }
        })
    }
  }
}
</script>

<style>
.post-writer {
  padding: 10px;
  margin-bottom: 12px;
}

.post-writer .container-fluid {
  padding: 0;
}

.post-writer form {
  margin-bottom: 12px;
}
</style>
