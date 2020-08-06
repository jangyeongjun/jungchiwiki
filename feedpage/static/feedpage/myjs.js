
$(document).ready(() => {
    
    $(".popup").click(() => {
        $("#test").fadeToggle(
        );
        
    });

    $(".normalFeed-down").click((e) => {
        const $this = $(e.currentTarget);
        const $down_form = $this.parent().parent().siblings('.normal-feed__supporting-text');
        const $up_arrow = $this.siblings('.normalFeed-up')
        $($down_form).fadeToggle(
            100
        );
        $($up_arrow).fadeToggle(
            0
        );
        $($this).fadeToggle(
            0
        );
    });

    $(".smallFeed-down").click((e) => {
        const $this = $(e.currentTarget);
        const $down_form = $this.parent().parent().siblings('.small-feed__supporting-text');
        const $up_arrow = $this.siblings('.smallFeed-up')
        $($down_form).fadeToggle(
            100
        );
        $($up_arrow).fadeToggle(
            0
        );
        $($this).fadeToggle(
            0
        );
    });

    $(".law-down").click((e) => {
        const $this = $(e.currentTarget);
        const $down_form = $this.parent().parent().siblings('.law__supporting-text');
        const $up_arrow = $this.siblings('.law-up')
        $($down_form).fadeToggle(
            100
        );
        $($up_arrow).fadeToggle(
            0
        );
        $($this).fadeToggle(
            0
        );
    });

    $(".normalFeed-up").click((e) => {
        const $this = $(e.currentTarget);
        const $up_form = $this.parent().parent().siblings('.normal-feed__supporting-text');
        const $down_arrow = $this.siblings('.normalFeed-down')
        $($up_form).fadeToggle(
            100
        );
        $($down_arrow).fadeToggle(
            0
        );
        $($this).fadeToggle(
            0
        );
    });

    $(".smallFeed-up").click((e) => {
        const $this = $(e.currentTarget);
        const $up_form = $this.parent().parent().siblings('.small-feed__supporting-text');
        const $down_arrow = $this.siblings('.smallFeed-down')
        $($up_form).fadeToggle(
            100
        );
        $($down_arrow).fadeToggle(
            0
        );
        $($this).fadeToggle(
            0
        );
    });

    $(".law-up").click((e) => {
        const $this = $(e.currentTarget);
        const $up_form = $this.parent().parent().siblings('.law__supporting-text');
        const $down_arrow = $this.siblings('.law-down')
        $($up_form).fadeToggle(
            100
        );
        $($down_arrow).fadeToggle(
            0
        );
        $($this).fadeToggle(
            0
        );
    });

    $(".comment-edit").click((e) => {
        const $this = $(e.currentTarget);
        const $edit_form = $this.siblings('.comment-edit-form');
        $($edit_form).fadeToggle(
            500
        );
    });

    $(".ctc-edit").click((e) => {
        const $this = $(e.currentTarget);
        const $edit_form = $this.siblings('.ctc-edit-form');
        $($edit_form).fadeToggle(
            500
        );
    });
    
    $(".normalFeed-edit").click((e) => {
        const $this = $(e.currentTarget);
        const $form_parent = $this.parent().parent().siblings('.normal-feed__supporting-text');
        const $edit_form = $form_parent.find('.normalFeed-edit-form');
        $($edit_form).fadeToggle(
            500
        );
    });

    $(".smallFeed-edit").click((e) => {
        const $this = $(e.currentTarget);
        const $form_parent = $this.parent().parent().siblings('.small-feed__supporting-text');
        const $edit_form = $form_parent.find('.smallFeed-edit-form');
        $($edit_form).fadeToggle(
            500
        );
    });


    $(".scroll-down").click((e) => {
        const $this = $(e.currentTarget);
        const id = $this.data('id')-1;
        console.log(id);
        var normalFeeds = document.querySelectorAll("#normalFeed");
        var location = normalFeeds[id].offsetTop;
        console.log(location);
        
        window.scrollTo({top:location, behavior:'smooth'});
        
    });




    $(".normalFeed-Like").click((e) => {
        e.preventDefault();
        const $this = $(e.currentTarget);
        const pid = $this.data('pid');
        const nfid = $this.data('nfid');
        const csrfmiddlewaretoken = $this.data('csrfmiddlewaretoken');
        $.ajax({
            url: `/feeds/politician/${pid}/normalfeed/${nfid}/like/`,
            type: "POST",
            data: {
                pid: pid,
                nfid: nfid,
                csrfmiddlewaretoken: csrfmiddlewaretoken,
            },
            dataType: "json",
            success: function(response) {
                console.log(response);
                const $dislike_button = $this.siblings('.normalFeed-Dislike'); 
                const dislike_count = parseInt($dislike_button.attr('data-badge'));
                const like_count = parseInt($this.attr('data-badge'));
                if(response.like_count > 0) {
                    $this.attr('data-badge', like_count+1);
                    if(response.dislike_count == 1){
                        $dislike_button.attr('data-badge', dislike_count-1);        
                    }
                    
                } else {
                    $this.attr('data-badge', like_count-1);
                }    
            },
            error: function(response, status, error) {
                console.log(response, status, error);
            },
            complete: function(response) {
                console.log(response);
            
            
            }

        })
    });

    $(".normalFeed-Dislike").click((e) => {
        e.preventDefault();
        const $this = $(e.currentTarget);
        const pid = $this.data('pid');
        const nfid = $this.data('nfid');
        const csrfmiddlewaretoken = $this.data('csrfmiddlewaretoken');
        $.ajax({
            url: `/feeds/politician/${pid}/normalfeed/${nfid}/dislike/`,
            type: "POST",
            data: {
                pid: pid,
                nfid: nfid,
                csrfmiddlewaretoken: csrfmiddlewaretoken,
            },
            dataType: "json",
            success: function(response) {
                console.log(response);
                const $like_button = $this.siblings('.normalFeed-Like'); 
                const like_count = parseInt($like_button.attr('data-badge'));
                const dislike_count = parseInt($this.attr('data-badge'));
                if(response.dislike_count > 0) {
                    $this.attr('data-badge', dislike_count+1);
                    if(response.like_count == 1){
                        $like_button.attr('data-badge', like_count-1);        
                    }
                    
                } else {
                    $this.attr('data-badge', dislike_count-1);
                }    
            },
            error: function(response, status, error) {
                console.log(response, status, error);
            },
            complete: function(response) {
                console.log(response);
            }
        })
    });


    $(".smallFeed-Like").click((e) => {
        e.preventDefault();
        const $this = $(e.currentTarget);
        const pid = $this.data('pid');
        const nfid = $this.data('nfid');
        const sfid = $this.data('sfid');
        const csrfmiddlewaretoken = $this.data('csrfmiddlewaretoken');
        $.ajax({
            url: `/feeds/politician/${pid}/normalfeed/${nfid}/smallfeed/${sfid}/like/`,
            type: "POST",
            data: {
                pid: pid,
                nfid: nfid,
                sfid: sfid,
                csrfmiddlewaretoken: csrfmiddlewaretoken,
            },
            dataType: "json",
            success: function(response) {
                console.log(response);
                const $dislike_button = $this.siblings('.smallFeed-Dislike'); 
                const dislike_count = parseInt($dislike_button.attr('data-badge'));
                const like_count = parseInt($this.attr('data-badge'));
                if(response.like_count > 0) {
                    $this.attr('data-badge', like_count+1);
                    if(response.dislike_count == 1){
                        $dislike_button.attr('data-badge', dislike_count-1);        
                    }
                    
                } else {
                    $this.attr('data-badge', like_count-1);
                }    
            },
            error: function(response, status, error) {
                console.log(response, status, error);
            },
            complete: function(response) {
                console.log(response);
            }
        })
    });

    $(".smallFeed-Dislike").click((e) => {
        e.preventDefault();
        const $this = $(e.currentTarget);
        const pid = $this.data('pid');
        const nfid = $this.data('nfid');
        const sfid = $this.data('sfid');
        const csrfmiddlewaretoken = $this.data('csrfmiddlewaretoken');
        $.ajax({
            url: `/feeds/politician/${pid}/normalfeed/${nfid}/smallfeed/${sfid}/dislike/`,
            type: "POST",
            data: {
                pid: pid,
                nfid: nfid,
                sfid: sfid,
                csrfmiddlewaretoken: csrfmiddlewaretoken,
            },
            dataType: "json",
            success: function(response) {
                console.log(response);
                const $like_button = $this.siblings('.smallFeed-Like'); 
                const like_count = parseInt($like_button.attr('data-badge'));
                const dislike_count = parseInt($this.attr('data-badge'));
                if(response.dislike_count > 0) {
                    $this.attr('data-badge', dislike_count+1);
                    if(response.like_count == 1){
                        $like_button.attr('data-badge', like_count-1);        
                    }
                    
                } else {
                    $this.attr('data-badge', dislike_count-1);
                }    
            },
            error: function(response, status, error) {
                console.log(response, status, error);
            },
            complete: function(response) {
                console.log(response);
            }
        })
    });


    $(".comment-Like").click((e) => {
        e.preventDefault();
        const $this = $(e.currentTarget);
        const pid =   $this.data('pid');
        const nfid =  $this.data('nfid');
        const cid =   $this.data('cid');
        const csrfmiddlewaretoken = $this.data('csrfmiddlewaretoken');
        $.ajax({
            url: `/feeds/politician/${pid}/normalfeed/${nfid}/debate/comment/${cid}/like/`,
            type: "POST",
            data: {
                pid: pid,
                nfid: nfid,
                cid: cid,
                csrfmiddlewaretoken: csrfmiddlewaretoken,
            },
            dataType: "json",
            success: function(response) {
                console.log(response);
                const $dislike_button = $this.siblings('.comment-Dislike'); 
                const dislike_count = parseInt($dislike_button.attr('data-badge'));
                const like_count = parseInt($this.attr('data-badge'));
                if(response.like_count > 0) {
                    $this.attr('data-badge', like_count+1);
                    if(response.dislike_count == 1){
                        $dislike_button.attr('data-badge', dislike_count-1);        
                    }
                    
                } else {
                    $this.attr('data-badge', like_count-1);
                }    
            },
            error: function(response, status, error) {
                console.log(response, status, error);
            },
            complete: function(response) {
                console.log(response);
            }
        })
    });

    $(".comment-Dislike").click((e) => {
        e.preventDefault();
        const $this = $(e.currentTarget);
        const pid =   $this.data('pid');
        const nfid =  $this.data('nfid');
        const cid =   $this.data('cid');
        const csrfmiddlewaretoken = $this.data('csrfmiddlewaretoken');
        $.ajax({
            url: `/feeds/politician/${pid}/normalfeed/${nfid}/debate/comment/${cid}/dislike/`,
            type: "POST",
            data: {
                pid: pid,
                nfid: nfid,
                cid: cid,
                csrfmiddlewaretoken: csrfmiddlewaretoken,
            },
            dataType: "json",
            success: function(response) {
                console.log(response);
                const $like_button = $this.siblings('.comment-Like'); 
                const like_count = parseInt($like_button.attr('data-badge'));
                const dislike_count = parseInt($this.attr('data-badge'));
                if(response.dislike_count > 0) {
                    $this.attr('data-badge', dislike_count+1);
                    if(response.like_count == 1){
                        $like_button.attr('data-badge', like_count-1);        
                    }
                    
                } else {
                    $this.attr('data-badge', dislike_count-1);
                }    
            },
            error: function(response, status, error) {
                console.log(response, status, error);
            },
            complete: function(response) {
                console.log(response);
            }
        })
    });


    $(".ctc-Like").click((e) => {
        e.preventDefault();
        const $this = $(e.currentTarget);
        const pid =   $this.data('pid');
        const nfid =  $this.data('nfid');
        const cid =   $this.data('cid');
        const ctcid = $this.data('ctcid');
        const csrfmiddlewaretoken = $this.data('csrfmiddlewaretoken');
        $.ajax({
            url: `/feeds/politician/${pid}/normalfeed/${nfid}/debate/comment/${cid}/ctc/${ctcid}/like/`,
            type: "POST",
            data: {
                pid: pid,
                nfid: nfid,
                cid: cid,
                ctcid: ctcid,
                csrfmiddlewaretoken: csrfmiddlewaretoken,
            },
            dataType: "json",
            success: function(response) {
                console.log(response);
                const $dislike_button = $this.siblings('.ctc-Dislike'); 
                const dislike_count = parseInt($dislike_button.attr('data-badge'));
                const like_count = parseInt($this.attr('data-badge'));
                if(response.like_count > 0) {
                    $this.attr('data-badge', like_count+1);
                    if(response.dislike_count == 1){
                        $dislike_button.attr('data-badge', dislike_count-1);        
                    }
                    
                } else {
                    $this.attr('data-badge', like_count-1);
                }    
            },
            error: function(response, status, error) {
                console.log(response, status, error);
            },
            complete: function(response) {
                console.log(response);
            }
        })
    });

    $(".ctc-Dislike").click((e) => {
        e.preventDefault();
        const $this = $(e.currentTarget);
        const pid =   $this.data('pid');
        const nfid =  $this.data('nfid');
        const cid =   $this.data('cid');
        const ctcid = $this.data('ctcid');
        const csrfmiddlewaretoken = $this.data('csrfmiddlewaretoken');
        $.ajax({
            url: `/feeds/politician/${pid}/normalfeed/${nfid}/debate/comment/${cid}/ctc/${ctcid}/dislike/`,
            type: "POST",
            data: {
                pid: pid,
                nfid: nfid,
                cid: cid,
                ctcid: ctcid,
                csrfmiddlewaretoken: csrfmiddlewaretoken,
            },
            dataType: "json",
            success: function(response) {
                console.log(response);
                const $like_button = $this.siblings('.ctc-Like'); 
                const like_count = parseInt($like_button.attr('data-badge'));
                const dislike_count = parseInt($this.attr('data-badge'));
                if(response.dislike_count > 0) {
                    $this.attr('data-badge', dislike_count+1);
                    if(response.like_count == 1){
                        $like_button.attr('data-badge', like_count-1);        
                    }
                    
                } else {
                    $this.attr('data-badge', dislike_count-1);
                }    
            },
            error: function(response, status, error) {
                console.log(response, status, error);
            },
            complete: function(response) {
                console.log(response);
            }
        })
    });


    $(".law-Like").click((e) => {
        e.preventDefault();
        const $this = $(e.currentTarget);
        const pid =   $this.data('pid');
        const lid =   $this.data('lid');
        const csrfmiddlewaretoken = $this.data('csrfmiddlewaretoken');
        $.ajax({
            url: `/feeds/politician/${pid}/law/${lid}/like/`,
            type: "POST",
            data: {
                lid: lid,
                csrfmiddlewaretoken: csrfmiddlewaretoken,
            },
            dataType: "json",
            success: function(response) {
                console.log(response);
                const $dislike_button = $this.siblings('.law-Dislike'); 
                const dislike_count = parseInt($dislike_button.attr('data-badge'));
                const like_count = parseInt($this.attr('data-badge'));
                if(response.like_count > 0) {
                    $this.attr('data-badge', like_count+1);
                    if(response.dislike_count == 1){
                        $dislike_button.attr('data-badge', dislike_count-1);        
                    }
                    
                } else {
                    $this.attr('data-badge', like_count-1);
                }    
            },
            error: function(response, status, error) {
                console.log(response, status, error);
            },
            complete: function(response) {
                console.log(response);
            }
        })
    });

    $(".law-Dislike").click((e) => {
        e.preventDefault();
        const $this = $(e.currentTarget);
        const pid =   $this.data('pid');
        const lid =   $this.data('lid');
        const csrfmiddlewaretoken = $this.data('csrfmiddlewaretoken');
        $.ajax({
            url: `/feeds/politician/${pid}/law/${lid}/dislike/`,
            type: "POST",
            data: {
                lid: lid,
                csrfmiddlewaretoken: csrfmiddlewaretoken,
            },
            dataType: "json",
            success: function(response) {
                console.log(response);
                const $like_button = $this.siblings('.law-Like'); 
                const like_count = parseInt($like_button.attr('data-badge'));
                const dislike_count = parseInt($this.attr('data-badge'));
                if(response.dislike_count > 0) {
                    $this.attr('data-badge', dislike_count+1);
                    if(response.like_count == 1){
                        $like_button.attr('data-badge', like_count-1);        
                    }
                    
                } else {
                    $this.attr('data-badge', dislike_count-1);
                }    
            },
            error: function(response, status, error) {
                console.log(response, status, error);
            },
            complete: function(response) {
                console.log(response);
            }
        })
    });

    $(".law-comment-Like").click((e) => {
        e.preventDefault();
        const $this = $(e.currentTarget);
        const pid =   $this.data('pid');
        const lid =   $this.data('lid');
        const cid =   $this.data('cid');
        const csrfmiddlewaretoken = $this.data('csrfmiddlewaretoken');
        $.ajax({
            url: `/feeds/politician/${pid}/law/${lid}/debate/comment/${cid}/like/`,
            type: "POST",
            data: {
                pid: pid,
                lid: lid,
                cid: cid,
                csrfmiddlewaretoken: csrfmiddlewaretoken,
            },
            dataType: "json",
            success: function(response) {
                console.log(response);
                const $dislike_button = $this.siblings('.law-comment-Dislike'); 
                const dislike_count = parseInt($dislike_button.attr('data-badge'));
                const like_count = parseInt($this.attr('data-badge'));
                if(response.like_count > 0) {
                    $this.attr('data-badge', like_count+1);
                    if(response.dislike_count == 1){
                        $dislike_button.attr('data-badge', dislike_count-1);        
                    }
                    
                } else {
                    $this.attr('data-badge', like_count-1);
                }    
            },
            error: function(response, status, error) {
                console.log(response, status, error);
            },
            complete: function(response) {
                console.log(response);
            }
        })
    });

    $(".law-comment-Dislike").click((e) => {
        e.preventDefault();
        const $this = $(e.currentTarget);
        const pid =   $this.data('pid');
        const lid =   $this.data('lid');
        const cid =   $this.data('cid');
        const csrfmiddlewaretoken = $this.data('csrfmiddlewaretoken');
        $.ajax({
            url: `/feeds/politician/${pid}/law/${lid}/debate/comment/${cid}/dislike/`,
            type: "POST",
            data: {
                pid: pid,
                lid: lid,
                cid: cid,
                csrfmiddlewaretoken: csrfmiddlewaretoken,
            },
            dataType: "json",
            success: function(response) {
                console.log(response);
                const $like_button = $this.siblings('.law-comment-Like'); 
                const like_count = parseInt($like_button.attr('data-badge'));
                const dislike_count = parseInt($this.attr('data-badge'));
                if(response.dislike_count > 0) {
                    $this.attr('data-badge', dislike_count+1);
                    if(response.like_count == 1){
                        $like_button.attr('data-badge', like_count-1);        
                    }
                    
                } else {
                    $this.attr('data-badge', dislike_count-1);
                }    
            },
            error: function(response, status, error) {
                console.log(response, status, error);
            },
            complete: function(response) {
                console.log(response);
            }
        })
    });

    
    $(".law-ctc-Like").click((e) => {
        e.preventDefault();
        const $this = $(e.currentTarget);
        const pid =   $this.data('pid');
        const lid =  $this.data('lid');
        const cid =   $this.data('cid');
        const ctcid = $this.data('ctcid');
        const csrfmiddlewaretoken = $this.data('csrfmiddlewaretoken');
        $.ajax({
            url: `/feeds/politician/${pid}/law/${lid}/debate/comment/${cid}/ctc/${ctcid}/like/`,
            type: "POST",
            data: {
                pid: pid,
                lid: lid,
                cid: cid,
                ctcid: ctcid,
                csrfmiddlewaretoken: csrfmiddlewaretoken,
            },
            dataType: "json",
            success: function(response) {
                console.log(response);
                const $dislike_button = $this.siblings('.law-ctc-Dislike'); 
                const dislike_count = parseInt($dislike_button.attr('data-badge'));
                const like_count = parseInt($this.attr('data-badge'));
                if(response.like_count > 0) {
                    $this.attr('data-badge', like_count+1);
                    if(response.dislike_count == 1){
                        $dislike_button.attr('data-badge', dislike_count-1);        
                    }
                    
                } else {
                    $this.attr('data-badge', like_count-1);
                }    
            },
            error: function(response, status, error) {
                console.log(response, status, error);
            },
            complete: function(response) {
                console.log(response);
            }
        })
    });

    $(".law-ctc-Dislike").click((e) => {
        e.preventDefault();
        const $this = $(e.currentTarget);
        const pid =   $this.data('pid');
        const lid =   $this.data('lid');
        const cid =   $this.data('cid');
        const ctcid = $this.data('ctcid');
        const csrfmiddlewaretoken = $this.data('csrfmiddlewaretoken');
        $.ajax({
            url: `/feeds/politician/${pid}/law/${lid}/debate/comment/${cid}/ctc/${ctcid}/dislike/`,
            type: "POST",
            data: {
                pid: pid,
                lid: lid,
                cid: cid,
                ctcid: ctcid,
                csrfmiddlewaretoken: csrfmiddlewaretoken,
            },
            dataType: "json",
            success: function(response) {
                console.log(response);
                const $like_button = $this.siblings('.law-ctc-Like'); 
                const like_count = parseInt($like_button.attr('data-badge'));
                const dislike_count = parseInt($this.attr('data-badge'));
                if(response.dislike_count > 0) {
                    $this.attr('data-badge', dislike_count+1);
                    if(response.like_count == 1){
                        $like_button.attr('data-badge', like_count-1);        
                    }
                    
                } else {
                    $this.attr('data-badge', dislike_count-1);
                }    
            },
            error: function(response, status, error) {
                console.log(response, status, error);
            },
            complete: function(response) {
                console.log(response);
            }
        })
    });

    $('#lawsearch_form').submit((event) => {
        event.preventDefault()
        console.log('lawsearch start')
        $.ajax({
            url: `/feeds/lawsearch/`,
            method: 'POST',
            dataType: 'json',
            data: {
                csrfmiddlewaretoken: $(event.currentTarget).data('csrfmiddlewaretoken'),
                lawsearch_key: $(`input#lawsearch_key`).val(),
            },
            success(response) {
                console.log(response)
            },
            error(response, status, error) {
                console.log(response, status, error)
            }
        })
      
          
      })



  }
);

