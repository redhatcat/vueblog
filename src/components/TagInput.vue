<template>
  <span class="b-tagsinput">
    <b-form-input
       v-bind="$attrs"
      :class='inputClass'
      v-model="localValue"/>
    <input
      type="hidden"
       v-on="$listeners"
      v-model="value"/>
  </span>
</template>

<script>
export default {
  name: 'TagInput',
  props: ['value'],
  data () {
    return {
      localValue: this.value
    }
  },
  methods: {
    updateValue: function (value) {
      var formattedValue = value
        // Remove whitespace on either side
        .trim()
        // Shorten to 2 decimal places
        .slice(
          0,
          value.indexOf('.') === -1
            ? value.length
            : value.indexOf('.') + 3
        )
      // If the value was not already normalized,
      // manually override it to conform
      if (formattedValue !== value) {
        this.$refs.input.value = formattedValue
      }
      // Emit the number value through the input event
      this.$emit('input', Number(formattedValue))
    }
  }
}
</script>

<style>
.b-tagsinput input {
  border: none;
  box-shadow: none;
  outline: none;
  background-color: transparent;
  padding: 0 6px;
  margin: 0;
  width: auto;
  max-width: inherit;
}

.b-tagsinput input {
  border: none;
  box-shadow: none;
  outline: none;
  background-color: transparent;
  padding: 0 6px;
  margin: 0;
  width: auto;
  max-width: inherit;
}

.b-tagsinput .tag {
  margin-right: 2px;
  color: white;
}

</style>
