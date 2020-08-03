
// $('#feed-create').submit((e) => {
//     e.preventDefault() 
//     const $this = $(e.currentTarget);
//     const pid = $this.data('pid');
//     const csrfmiddlewaretoken = $this.data('csrfmiddlewaretoken');
//     $.ajax({
//       url: `/feeds/politician/${pid}/normalfeed/new/`,  // feed create을 POST 받는 url과, view함수는 "/feeds/"였습니다. 
//       method: 'POST',
//       data: {  // 요청(request)로 함께 보낼 데이터 정의
//         pid : pid,
//         title: $(`input#title`).val(),
//         content: $(`textarea#content-text`).val(),
//         csrfmiddlewaretoken: csrfmiddlewaretoken   // 장고 security와 관련해서 아무나 feed를 생성하지 못하도록 form 액션을 할 때는, csrf_token이 필요
//       },
//       dataType: "json",  // json => "javascript object notation"
//       success(response) {
//         console.log(response)
//         str = `
//         <div class="demo-card-wide mdl-card mdl-shadow--2dp normal-feed" id ="normalFeed">
//             <div class="mdl-card__title">
//                 <h2>${response.title}.${response.newNormalFeed.get_title_display}</h2>

//                 <a href="/feeds/politician/${pid}/normalfeed/${response.id}/like/" 
//                 class = "material-icons mdl-badge normalFeed-Like"  
//                 data-pid=${pid} 
//                 data-nfid=${response.id} 
//                 data-csrfmiddlewaretoken="${csrfmiddlewaretoken}"
//                 data-badge="${response.newNormalFeed.like_users.count}">LIKE</a>

//                 <a href="/feeds/politician/${pid}/normalfeed/${response.id}/dislike/" 
//                 class = "material-icons mdl-badge normalFeed-Dislike"  
//                 data-pid=${pid} 
//                 data-nfid=${response.id }
//                 data-csrfmiddlewaretoken="${csrfmiddlewaretoken}" 
//                 data-badge="${response.newNormalFeed.dislike_users.count}">DISLIKE</a>

//                 <a href="/feeds/politician/${pid}/normalfeed/${response.id}/debate/">해당 내용에 대한 토론방</a>
//             </div>
//         </div>
//         `
//         $(str).insertBefore($this);
//       },
//       error(response, status, error) {
//         console.log(response, status, error);
//       }
//     })
// })




// $('#signup-form').submit((event) => {
//     event.preventDefault()
//     $.ajax({
//         url: '/accounts/signup/',
//         method: 'POST',
//         dataType: 'json',
//         data: {
//             csrfmiddlewaretoken: $(event.currentTarget).data('csrfmiddlewaretoken'),
//             username: $(`input#username`).val(),
//             // email: $(`input#email`).val(),
//             password1: $(`input#password1`).val(),
//             password2: $(`input#password2`).val(),
//             gender: $(`input#gender`).val(),
//             politicalOrientation: $(`input#politicalOrientation`).val()
//         },
//         success(response) {
//             console.log(response)
//             window.location.href='/feeds/'
//         },
//         error(response, status, error) {
//             console.log(response, status, error)
//         }
//     })

    
// })