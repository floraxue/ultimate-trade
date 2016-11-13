function ApiRequest(){

}

ApiRequest.signup = function(email, username, pwd1, pwd2){
    //login ApiRequest
    //input:
    //email: users' email address
    //username: user's username
    //password; user's password
    //returned:
    //"success":true if signup success, otherwise false.
    //"error": if not success, return error message, otherwise, empty string.
    var dictionary = {};
    if(pwd1!==pwd2){
      dictionary["success"] = false;
      dictionary["error"] = "Password not match"
    }
    $.ajax({
    		url: "register",
    		dataType: "json",
    		type: "post",
    		data: {
    			"email":email,
    			"username":username,
    			"pwd1":pwd1,
    			"pwd2":pwd2
    		},
    		success: function(data){
          dictionary["success"] = data["success"];
          dictionary["error"] = data["error"];
          console.log("success");
  			},
  			failure: function(errMsg) {
  				console.log("server no response");
  			}
  		});
      return dictionary;
}

ApiRequest.login = function(username, pwd1){
    //login ApiRequest
    //input:
    //username: user's username
    //password; user's password
    //returned:
    //"success":true if login success, otherwise false.
    //"error": if not success, return error message, otherwise, empty string.
    var dictionary = {};
    $.ajax({
    		url: " ",
    		dataType: "json",
    		type: "post",
    		data: {
    			"username":username,
    			"pwd":pwd
    		},
    		success: function(data){
          dictionary["success"] = data["success"];
          dictionary["error"] = data["error"];
  			},
  			failure: function(errMsg) {
  				console.log("server no response");
  			}
  		});
      return dictionary;
}

ApiRequest.getItems = function(category){
  //login ApiRequest
  //input:
  //category: item category
  //output:
  // item:
  //    itemID:
  //    title:
  //    itemimage:
  //    releaseData:
  //    seller username;
  // item:
  //    itemID:
  //    title:
  //    itemimage:
  //    releaseDate:
  //    seller username;
  //......
  var dictionary = {};
  $.ajax({
      url: " ",
      dataType: "json",
      type: "post",
      data: {
        "category":username
      },
      success: function(data){
        for(var i in data){
           var id = data[i].itemID;
           var title = data[i].title;
           var name = data[i].itemimage;
           var releaseDate = data[i].releaseDate;
           var username = data[i].username;
           var item = new ItemInList(id,name,releaseDate,username);
           items.push(item);
         }
      },
      failure: function(errMsg) {
        console.log("server no response");
      }
    });
    $("#itemListPage").empty();
    for(item in items){
      var container = $("<div>");
      $( "#itemListPage" ).append(container);
      container.addClass("item");
      container.attr('id', item.itemID);

      var titleDiv = $("</div>");
      h1.text(item.title);
      h1.addClass("itemTitle");
      container.append(titleDiv);

      var image = $("<img>");
      image.addClass("itemImage");
      image.attr('src',item.image);
      container.append(h1);

      var dateDiv = $("</div>");
      h1.text(item.releaseDate);
      h1.addClass("itemDate");
      container.append(dateDiv);

      var sellerDiv = $("</div>");
      h1.text("from"+item.username);
      h1.addClass("itemSeller");
      container.append(sellerDiv);
    }
}