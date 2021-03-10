<template>
<input v-bind="attrs" :placeholder="weather" v-model="weather_location" v-on:keyup.enter="fetch_weather">
</template>

<script>
export default {
    props: {
        type: {
            type: String,
            default: 'text'
        },
        size: {
            type: Number,
            default: 30
        },
        title: {
            type: String,
            default: 'weather'
        },
    },
    data() {
        return {
            weather: null,
            weather_location: null
        }
    },
    computed: {
        attrs() {
            const attrs = {
                type: this.type,
                size: this.size,
                title: this.title,
                ...this.$attrs
            };
            return attrs;
        },
    },
    methods: {
        async fetch_weather() {
            let protocol = document.location.protocol;
            let location = this.weather_location ? this.weather_location : "milford haven"
            let url = `${protocol}//wttr.in/${location}?format=3`
            fetch(url)
                .then(async (response) => {
                    this.weather = await response.text()
                    this.weather_location = null
                })
        }
    },
    mounted() {
        this.fetch_weather()
    }
}
</script>
