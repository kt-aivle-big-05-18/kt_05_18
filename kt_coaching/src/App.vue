<template>
  <!-- <img alt="Vue logo" src="./assets/logo.png">
  <HelloWorld msg="Welcome to Your Vue.js App"/> -->
  <div>
      <Header></Header>
      <router-view></router-view>
      <Footer></Footer>
    </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
import Header from './layout/Header';
import Footer from './layout/Footer';

export default {
  name: 'App',
  components: {
    // HelloWorld
    Header,
    Footer,
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
