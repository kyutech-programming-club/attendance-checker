<template>
  <div class="attend">
    <h1>This is an attend page</h1>
    <v-layout justify-center>
      <v-container>
        <v-row>
          <v-col>
            <v-form>
              <v-input>
                <v-text-field
                  label="name">
                </v-text-field>
              </v-input>
            </v-form>
          </v-col>
        </v-row>
        <v-btn color="blue" class="ma-5">
          <v-icon left>
            mdi-login
          </v-icon>
          出席
        </v-btn>
        <v-btn color="red" class="ma-5">
          <v-icon left>
            mdi-logout
          </v-icon>
          退出
        </v-btn>
      </v-container>
    </v-layout>
  </div>
</template>
