<template>
<div class="HelloWorld">
    <div class="page">
        <Weather class="weather" />
        <div class="transcript" ref="transcript">
            <div class="line" v-for="(line, idx) in transcript" :key="idx">
                <template v-if="line.user == email">
                    <UserImage :email="line.user" class="circle" v-if="line.user == email" />
                    <div class="message">{{ line.message }}</div>
                    <div class="spacer"></div>
                </template>
                <template v-else>
                    <div class="spacer"></div>
                    <div class="message">{{ line.message }}</div>
                    <UserImage :email="line.user" class="circle" v-if="line.user != email" />
                </template>
            </div>
        </div>
        <form @submit.prevent="say">
            <UserImage :email="email" class="circle" v-if="email" />
            <input type="text" v-model="something" placeholder="say something" />
            <input type="submit" value="Say" />
        </form>
        <div class="status">
            {{ status }}
        </div>
    </div>
</div>
</template>

<script>
import UserImage from './user_image.vue'
import Weather from './weather.vue'
export default {
    components: {
        UserImage,
        Weather
    },
    data() {
        return {
            something: ""
        }
    },
    computed: {
        email() {
            return this.$ws.state.email
        },
        transcript() {
            return this.$ws.state.transcript
        },
        status() {
            return this.$ws.state.status
        }
    },
    methods: {
        say() {
            this.$ws.send(this.something)
            this.something = ""
        }
    },
    watch: {
        transcript: {
            handler(val) {
                setTimeout(() => {
                    this.$refs.transcript.scrollTop = this.$refs.transcript.scrollHeight
                }, 100)
            },
            deep: true
        }
    }
}
</script>

<style scoped>
.page {
    display: flex;
    flex-direction: column;
    height: 500px;
    margin: 0 1rem;
}

form {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: start;
}

form input[type=text] {
    flex-grow: 1;
    margin: 0 0.25rem;
    font-size: 1.2rem;
}

form input[type=submit] {
    font-size: 1.2rem;
}

.transcript {
    display: flex;
    flex-direction: column;
    margin-top: 0.5rem;
    overflow-y: auto;
}

.line {
    display: flex;
    flex-direction: row;
    align-items: center;
    margin-bottom: 0.5rem;
}

.line img,
form img {
    height: 1.6rem;
}

.message {
    text-align: left;
    padding: 0.5rem;
    background-color: #eee;
    border-radius: 8px;
}

.circle {
    border-radius: 50%;
    border: 1px solid gray;
    margin: 2px;
}

.spacer {
    flex-grow: 1;
    min-width: 40%;
}

.status {
    font-size: small;
    color: gray;
    text-align: left;
    padding-left: 2.5rem;
}

.weather {
    align-self: center;
}
</style>
