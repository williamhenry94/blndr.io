
new Vue({
    el: '#stack-questions',
    data () {
      active= true;
      return {
        
        stack_questions: null
      }
    },
    methods:{
      showComments(event){
         let repoId = event.target.dataset.repoId;
         axios
          .get('/api/rating/'+repoId)
          .then((res)=>{
            console.log(res);
          })
      }
    },
    computed:{
        isActive: function (){
          return {active:active}
      } 
      
    },
    mounted () {
      axios
        .get('/api/stackoverflow')
        .then(response => {
          
            this.stack_questions = response.data.items.slice(0,10)
        })
    }
  });

 