function LoadComponent(){

}

LoadComponent.loadHeader = function(){
  $( "#header" ).load( "header.html", function() {
    console.log( "Load header was performed." );
  });
}

LoadComponent.loadMainPage = function(){
  $( "#mainPage" ).load( "mainPage.html", function() {
    console.log( "Load mainPage was performed." );
  });
}

LoadComponent.loadAcoountPage = function(){
  $( "#accountPage" ).load( "accountPage.html", function() {
    console.log( "Load account was performed." );
  });
}

LoadComponent.loaditemUploadPage = function(){
  $( "#itemUpload" ).load( "itemUploadPage.html", function() {
    console.log( "Load itemUpload was performed." );
  });
}

LoadComponent.loadsignUpPage = function(){
  $( "#signupPage" ).load( "signupPage.html", function() {
    console.log( "Load signupPage was performed." );
  });
}

LoadComponent.loadLoginSignup = function(loggedin){
  if(loggedin=="true"){
    $("#loginSignUpContainer").load("goToPortalButtom.html",function(){
      console.log( "Load signupLogin was performed." );
    });
  }else{
    $("#loginSignUpContainer").load("login_signup_buttom.html",function(){
      console.log( "Load goPortal was performed." );
    });
  }
}
