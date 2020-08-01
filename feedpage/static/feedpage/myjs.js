
$(document).ready(() => {
    $(".popup").mouseenter(() => {
        $("#test").fadeToggle(
            1000
        );
    });
    
    $(".scroll-down").click((e) => {
        const $this = $(e.currentTarget);
        const id = $this.data('id')-1;
        var normalFeeds = document.querySelectorAll("#normalFeed");
        var location = normalFeeds[id].offsetTop;
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
                const count = parseInt($this.attr('data-badge'));
                if(response.like_count > 0) {
                    $this.attr('data-badge', count+1);
                } else {
                    $this.attr('data-badge', count-1);
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
                    $like_button.attr('data-badge', like_count-1);
                } else {
                    $this.attr('data-badge', dislike_count-1);
                    $like_button.attr('data-badge', like_count+1);
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

  }
);


function setPage(listCount, currentPage, kwd) {
    var kwd = kwd; // 검색어
    var listCount = listCount;  // 전체 게시글 수
    var pageCount = (parseInt( listCount/ 10) + 1); // 페이지 개수
    var currentPage = currentPage; // 현재 페이지
    var endPage = (parseInt(pageCount/10 + 1) * 5)+1; // 최종 페이지
    var displayPage = parseInt((currentPage + 4 ) / 5 ) * 5; // 밑에 보여줄 페이지

    /* 게시글 수가 페이지 수와 딱 맞을 땐 다음 페이지 안보이게*/
    if(parseInt( listCount% 10)==0){
        pageCount -=1;
    };
    console.log("listCount", listCount);
    console.log("pageCount", pageCount);
    console.log("currentPage", currentPage);
    console.log("endPage", endPage);
    console.log("displayPage", displayPage);

    var pager = $('#pager');
        if(currentPage <= 5){
        pager.prepend('<li>◀</li>');
    }else{
        pager.append('<li><a href=/board/list/'+(displayPage-5)+'?kwd='+kwd+'>'+'◀'+'</li>');
    }

    for (var i = displayPage-4; i <= displayPage; i++) {
        if(i==currentPage){
            pager.append('<li class="selected">'+i+'</li>')
            continue;
        }else if(i>pageCount){
            pager.append('<li>'+i+'</li>')
            continue;
        }
        pager.append('<li><a href=/board/list/'+i+'?kwd='+kwd+'>'+i+'</li>');
    }

    var nextPage = displayPage+1

    if(currentPage < endPage && endPage < pageCount){
        pager.append('<li><a href=/board/list/'+nextPage+ '?kwd='+kwd+'>'+'▶'+'</li>');
    }else{
        pager.append('<li>'+'▶'+'</li>');
}

}