
new Vue({
    el: '#markdown',
    data () {
      return {
        markdown: null
      }
    },
    mounted(){
        var md = window.markdownit();
        var result = md.render(this.$el.dataset.md);
        
        this.markdown = result;
        this.$el.dataset.md = '';
    }
  });