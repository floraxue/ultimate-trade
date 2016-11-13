function SetCookies(){

}

SetCookies.login(userId){
  $.cookie('userId',userId);
  $.cookie('loggedin', true)
}
