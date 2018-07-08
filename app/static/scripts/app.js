new Vue({
    el: '#project-highlights',
    data () {
        
      return {
        
        project_highlights: null
      }
    },
    methods:{
        languageIcon: function (language){
            console.log(language)
            if (language.toLowerCase() == 'javascript'){
                return "fab fa-js";
            }else  if (language.toLowerCase() == 'java'){
                return "fab fa-java";
            }else  if (language.toLowerCase() == 'python'){
                return "fab fa-python";
            }
        }
    },
    mounted () {
      axios
        .get('/repos')
        .then(response => {
            console.log(response)
            this.project_highlights = response.data
        })
    }
  });

 