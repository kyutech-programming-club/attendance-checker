<template>
  <div>
    <v-app-bar dark fixed app>
      <v-toolbar-title>
        <router-link to="/" class="toolbar-title">出欠チェッカー</router-link>
      </v-toolbar-title>

      <v-spacer />

      <v-app-bar-nav-icon
        @click.stop="drawer = !drawer"
        class="hidden-md-and-up"
      />

      <v-toolbar-items class="hidden-sm-and-down">
        <v-btn to="/">
          <v-icon>mdi-home</v-icon>
        </v-btn>
        <v-btn to="/about">
          <v-icon>mdi-information</v-icon>
        </v-btn>
        <v-btn to="/attend">
          <v-icon>mdi-fingerprint</v-icon>
        </v-btn>
      </v-toolbar-items>
    </v-app-bar>

    <v-navigation-drawer dark v-model="drawer" right temporary fixed>
      <v-list>
        <v-divider></v-divider>
        <v-list-item v-for="item in items" :key="item.title" :to="item.to">
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </div>
</template>
<script>
  export default {
    data() {
      return {
        drawer: null,
        items: [
          { title: 'Home', icon: 'mdi-home', to: '/' },
          { title: 'About', icon: 'mdi-information', to: '/about' },
          { title: 'Attend', icon: 'mdi-fingerprint', to: '/attend' }
        ]
      };
    }
  }
</script>
<style scoped>
  .toolbar-title {
    color: white;
    text-decoration: none;
  }
</style>
