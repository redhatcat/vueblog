export const addBlogItems = (state, items) => {
  state.blog.items = state.blog.items.concat(items)
}

export const prependBlogItems = (state, items) => {
  state.blog.items = items.concat(state.blog.items)
}

export const setBlogLoading = (state, isLoading) => {
  state.blog.loading = isLoading
}

export const setBlogFetchComplete = (state, value) => {
  state.blog.fetchComplete = value
}

export const setUserData = (state, loginResponse) => {
  state.user.username = loginResponse.username
  state.user.token = loginResponse.access_token
  state.UserLogin.error = ''
}

export const setUserInterval = (state, interval) => {
  state.user.interval = interval
}

export const setUserLoginError = (state, message) => {
  state.UserLogin.error = message
}

export const updateBlogItem = (state, updatedItem) => {
  let items = state.blog.items.slice()
  let newItems = []
  items.forEach(function (item) {
    if (item.id === updatedItem.id) {
      if (!updatedItem.trash) {
        newItems.push(updatedItem)
      }
    } else {
      newItems.push(item)
    }
  })
  state.blog.items = newItems
}

export const setTagFilter = (state, tags) => {
  state.blog.tags = tags
}

export const clearBlogItems = (state) => {
  state.blog.items = []
}
