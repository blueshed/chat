<template>
<img v-bind="attrs" :src="url" :alt="alt" @load="loaded" @error="error" :title="email" />
</template>

<script>
import md5 from 'md5';
export default {
    props: {
        email: {
            type: String,
            default: ''
        },
        size: {
            type: Number,
            default: 80
        },
        alt: {
            type: String,
            default: 'gravatar'
        },
        defaultImg: {
            type: String,
            default: 'robohash'
        },
        rating: {
            type: String,
            default: 'g'
        }
    },
    computed: {
        url() {
            let protocol = document.location.protocol;
            const img = [
                `${protocol}//www.gravatar.com/avatar/`,
                md5(this.email.trim().toLowerCase()),
                `?s=${this.size}`,
                `&d=${this.defaultImg}`,
                `&r=${this.rating}`,
            ];
            return img.join('')
        },
        attrs() {
            const { src, alt, ...attrs } = this.$attrs;
            return attrs;
        }
    },
    methods: {
        loaded(...args) {
            this.$emit('loaded', ...args);
        },
        error(...args) {
            this.$emit('error', ...args);
        }
    }
}
</script>

<style lang="css" scoped>
</style>
