<template>
<div class="page">
    <div class="transcript">
        <div class="line" v-for="line in $ws.transcript">
            {{ line }}
        </div>
    </div>
    <form @submit.prevent="say">
        <input type="text" v-model="name" placeholder="your name" size="10">
        <input type="text" v-model="something" placeholder="say something" size="40">
        <input type="submit" value="Say">
    </form>
</div>
</template>

<script>
export default {
    data() {
        return {
            name: "anon",
            something: ""
        }
    },
    methods: {
        say() {
            this.$ws.send(`${this.name} said: ${this.something}`)
            this.something = ""
        }
    }
}
</script>

<style scoped>
.page {
    display: flex;
    flex-direction: column;
}

.form {
    display: flex;
    flex-direction: row;
}

.transcript {
    display: flex;
    flex-direction: column;
}
</style>
