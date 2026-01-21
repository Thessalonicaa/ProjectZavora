<template>
  <div>
    <h1>Protected Route</h1>
    <!-- Add your protected content here -->
  </div>
</template>

<script>
export default {
  name: 'NavigationGuard',
  beforeCreate() {
    // Check if user is authenticated
    const token = localStorage.getItem('token')
    if (!token) {
      // Redirect to login if no token found
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
/* Add your styles here */
</style>