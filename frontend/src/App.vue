<template>
  <div >
  
  <router-view>

    
  </router-view>
  <!-- <FlashMessage /> -->
  <AppFooter/>

  </div>
</template>

<script>

import AppFooter from './components/AppFooter.vue'
// import FlashMessage from '@smartweb/vue-flash-message'

// this.flashMessage.show({
// 	status: 'error',
// 	title: 'Error Message Title',
// 	message: 'Oh, you broke my heart! Shame on you!'
// });

export default {
  components: {
    AppFooter,
    // FlashMessage
  }
}
</script>

<style>

</style>
