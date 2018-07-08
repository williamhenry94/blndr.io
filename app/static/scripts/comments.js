new Vue({
    el: '#comment-placeholder',
    data () {
        return {
           rating: "",
           application_name: "",
           comment: "",
           website: "",
           platform: "web",

           error_rating:"",
           error_application_name: "",
           error_comment: "",
           error_website: "",
           error_platform: ""
        }
    },
    methods:{
        sendComment: function(event){
            let repoId = event.target.dataset.repoId;
            let fullName = event.target.dataset.fullName;
            
            
            let data= {
                rating: this.rating,
                comment: this.comment,
                application_name: this.application_name,
            
                platform: this.platform,
                rating: parseInt(this.rating),
                repo_id: repoId
            }

            if (this.website!==""){
                data["website"] = this.website
            }

            axios
                .post("/api/rating/"+fullName, JSON.stringify(data), { headers: {
                    'Content-type': 'application/json',
                }})
                .then((response)=>{
                    
                    swal("Feedback Submitted", "", "success").then(()=>{
                        this.rating =  "";
                        this.application_name= "";
                        this.comment= "";
                        this.website= "";
                        this.platform= "web";

                        this.error_rating="";
                        this.error_application_name= "";
                        this.error_comment= "";
                        this.error_website= "";
                        this.error_platform= "";
                        $('#comment_modal').modal('hide');
                    });
                    
                }).catch((err)=>{

                    this.error_rating="";
                    this.error_application_name= "";
                    this.error_comment= "";
                    this.error_website= "";
                    this.error_platform= "";

                   
                    if (err.response.status ==400)
                        if ("rating" in err.response.data)
                            this.error_rating = err.response.data.rating
                        if ("comment" in err.response.data)
                            this.error_comment = err.response.data.comment
                        if ("application_name" in err.response.data)
                            this.error_application_name = err.response.data.application_name
                        if ("platform" in err.response.data)
                            this.error_platform = err.response.data.platform
                        if ("website" in err.response.data)
                            this.error_website = err.response.data.website
                    else if (err.response.status==403)
                        swal("Oops!", err.response.data.message, "error");
                  

                })
           
        }
    }
  });



 