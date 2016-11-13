Function search(){
  $( "#bedFrameSearch" ).click(function() {
    ApiRequest.getItems("bedFrame");
  });
  $( "#chairSearch" ).click(function() {
  ApiRequest.getItems("chair");
  });
  $( "#deskSearch" ).click(function() {
  ApiRequest.getItems("desk");
  });
  $( "#matressSearch" ).click(function() {
  ApiRequest.getItems("matressFrame");
  });

}
