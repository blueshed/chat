var t=Object.prototype.hasOwnProperty,e=Object.getOwnPropertySymbols,a=Object.prototype.propertyIsEnumerable,s=Object.assign;import{m as r,o,c as l,a as n,w as i,b as c,v as u,d,p as m,e as p,r as h,f,F as w,g,h as y,i as v,j as $,t as b,k as _,l as O}from"./vendor.f8958272.js";!function(t=".",e="__import__"){try{self[e]=new Function("u","return import(u)")}catch(a){const s=new URL(t,location),r=t=>{URL.revokeObjectURL(t.src),t.remove()};self[e]=t=>new Promise(((a,o)=>{const l=new URL(t,s);if(self[e].moduleMap[l])return a(self[e].moduleMap[l]);const n=new Blob([`import * as m from '${l}';`,`${e}.moduleMap['${l}']=m;`],{type:"text/javascript"}),i=Object.assign(document.createElement("script"),{type:"module",src:URL.createObjectURL(n),onerror(){o(new Error(`Failed to import: ${t}`)),r(i)},onload(){a(self[e].moduleMap[l]),r(i)}});document.head.appendChild(i)})),self[e].moduleMap={}}}("/assets/");const j={props:{email:{type:String,default:""},size:{type:Number,default:80},alt:{type:String,default:"gravatar"},defaultImg:{type:String,default:"robohash"},rating:{type:String,default:"g"}},computed:{url(){return[`${document.location.protocol}//www.gravatar.com/avatar/`,r(this.email.trim().toLowerCase()),`?s=${this.size}`,`&d=${this.defaultImg}`,`&r=${this.rating}`].join("")},attrs(){const s=this.$attrs,{src:r,alt:o}=s;return((s,r)=>{var o={};for(var l in s)t.call(s,l)&&r.indexOf(l)<0&&(o[l]=s[l]);if(null!=s&&e)for(var l of e(s))r.indexOf(l)<0&&a.call(s,l)&&(o[l]=s[l]);return o})(s,["src","alt"])}},methods:{loaded(...t){this.$emit("loaded",...t)},error(...t){this.$emit("error",...t)}}},S=i("data-v-31a1d7a4")(((t,e,a,s,r,i)=>(o(),l("img",n(i.attrs,{src:i.url,alt:a.alt,onLoad:e[1]||(e[1]=(...t)=>i.loaded&&i.loaded(...t)),onError:e[2]||(e[2]=(...t)=>i.error&&i.error(...t)),title:a.email}),null,16,["src","alt","title"]))));j.render=S,j.__scopeId="data-v-31a1d7a4";const U={props:{type:{type:String,default:"text"},size:{type:Number,default:30},title:{type:String,default:"weather"}},data:()=>({weather:null,weather_location:null}),computed:{attrs(){return s({type:this.type,size:this.size,title:this.title},this.$attrs)}},methods:{async fetch_weather(){let t=this.weather_location?this.weather_location:"milford haven";fetch(`http://wttr.in/${t}?format=3`).then((async t=>{this.weather=await t.text(),this.weather_location=null}))}},mounted(){this.fetch_weather()}};U.render=function(t,e,a,s,r,i){return c((o(),l("input",n(i.attrs,{placeholder:r.weather,"onUpdate:modelValue":e[1]||(e[1]=t=>r.weather_location=t),onKeyup:e[2]||(e[2]=d(((...t)=>i.fetch_weather&&i.fetch_weather(...t)),["enter"]))}),null,16,["placeholder"])),[[u,r.weather_location]])};const k={components:{UserImage:j,Weather:U},data:()=>({something:""}),computed:{email(){return this.$ws.state.email},transcript(){return this.$ws.state.transcript},status(){return this.$ws.state.status}},methods:{say(){this.$ws.send(this.something),this.something=""}},watch:{transcript:{handler(t){setTimeout((()=>{this.$refs.transcript.scrollTop=this.$refs.transcript.scrollHeight}),100)},deep:!0}}},L=i("data-v-14414341");m("data-v-14414341");const x={class:"HelloWorld"},I={class:"page"},R={class:"transcript",ref:"transcript"},z={class:"message"},M=f("div",{class:"spacer"},null,-1),E=f("div",{class:"spacer"},null,-1),P={class:"message"},W=f("input",{type:"submit",value:"Say"},null,-1),F={class:"status"};p();const N=L(((t,e,a,s,r,n)=>{const i=h("Weather"),u=h("UserImage");return o(),l("div",x,[f("div",I,[f(i,{class:"weather"}),f("div",R,[(o(!0),l(w,null,g(n.transcript,((e,a)=>(o(),l("div",{class:"line",key:a},[e.user==t.$ws.state.email?(o(),l(w,{key:0},[e.user==n.email?(o(),l(u,{key:0,email:e.user,class:"circle"},null,8,["email"])):v("",!0),f("div",z,b(e.message),1),M],64)):(o(),l(w,{key:1},[E,f("div",P,b(e.message),1),e.user!=n.email?(o(),l(u,{key:0,email:e.user,class:"circle"},null,8,["email"])):v("",!0)],64))])))),128))],512),f("form",{onSubmit:e[2]||(e[2]=y(((...t)=>n.say&&n.say(...t)),["prevent"]))},[n.email?(o(),l(u,{key:0,email:n.email,class:"circle"},null,8,["email"])):v("",!0),c(f("input",{type:"text","onUpdate:modelValue":e[1]||(e[1]=t=>r.something=t),placeholder:"say something"},null,512),[[$,r.something]]),W],32),f("div",F,b(n.status),1)])])}));k.render=N,k.__scopeId="data-v-14414341";const V=f("img",{alt:"Vue logo",src:"/favicon.ico"},null,-1);var C={install:(t,e)=>{console.log(e);let a=`${"https:"==document.location.protocol?"wss://":"ws://"}${`${document.domain}:${document.location.port}`}${e.url}`;const s=new WebSocket(a);s.state=_({status:"connecting",email:"",transcript:[]}),s.onopen=function(){s.state.status="connected"},s.onmessage=function(t){""==s.state.email?s.state.email=t.data:s.state.transcript.push(JSON.parse(t.data))},s.onclose=function(){s.state.status="disconnected"},t.config.globalProperties.$ws=s}};const H=O({expose:[],setup:t=>(t,e)=>(o(),l(w,null,[V,f(k)],64))});H.use(C,{url:"/ws"}),H.mount("#app");
