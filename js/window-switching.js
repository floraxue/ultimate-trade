function WindowSwitching(){

}

WindowSwitching.toPortal = function(){
  $("#itemListPage").fadeOut();
  $("#mainPage").fadeOut();
  $("#accountPage").fadeIn();
}

WindowSwitching.toItem = function(){
  $("#accountPage").fadeOut();
  $("#mainPage").fadeOut();
  $("#itemListPage").fadeIn();
}

WindowSwitching.toMain = function(){
  $("#accountPage").fadeOut();
  $("#itemListPage").fadeOut();
  $("#mainPage").fadeIn();
}
