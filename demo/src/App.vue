<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
  data () {
    return {
    }
  },
  mounted () {
  }
}
</script>

<style>
  @import "./assets/css/main.css";
  @import "./assets/css/color-dark.css";  /*深色主题*/
  /*@import "./assets/css/theme-green/color-green.css"; */  /*浅绿色主题*/

  .el-upload__input {
    display: none;
  }
  input[type=file] {
    display: none;
  }
  .el-upload--text {
    width: 80px;
    height: 34px;
    border: 0;
    overflow: visible;
  }
</style>
