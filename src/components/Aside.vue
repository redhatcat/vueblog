<template>
  <aside class="aside-menu">
    <div class="m-0 py-2 text-muted text-center bg-light text-uppercase">
       <small><b>Frontend build version</b></small>
    </div>
    <div class="m-0 py-2 text-center bg-light text-uppercase">
       <small><b>{{ version }}</b></small>
    </div>
  </aside>
</template>

<script>
import version from '@/version.js'

export default {
  name: 'c-aside',
  data () {
    return {
      version: version.version
    }
  }
}
</script>
