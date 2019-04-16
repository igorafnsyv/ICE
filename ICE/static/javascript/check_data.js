let username = document.getElementById('id_username');
let password1 = document.getElementById('id_password1');
let password2 = document.getElementById('id_password2');
let result = true;


    function checkData(){

        if (username.value=="" || password1.value=="" || password2.value==""){
            document.getElementById('error').innerHTML="Please, do not leave the fields blank";
            return false;
        }

        if (!isNaN(password1.value)) {
            document.getElementById('error').innerHTML="Your password can't be entirely numeric";
            password1.value="";
            password2.value="";
            return false;
        }
        if ((password1.value + "").length < 8) {
            document.getElementById('error').innerHTML="Your password must contain at least 8 characters.";
            password1.value="";
            password2.value="";
            return false;
        }
        if (username.value.includes(password1.value) || password1.value.includes(username.value)) {
            document.getElementById('error').innerHTML="Your password can't be too similar to your other personal information.";
            password1.value="";
            password2.value="";
            return false;
        }
        if (password1.value != password2.value) {
            document.getElementById('error').innerHTML="Passwords do not match";
            password1.value="";
            password2.value="";
            return false;
        }
        checkUsername();
        return result;



    }

    function checkUsername() {
      let xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange=function() {
        if (this.readyState == 4 && this.status == 200) {
            if (this.response == "False") {
                document.getElementById("error").innerHTML = "This username already exists";
                username.value="";
                password1.value="";
                password2.value="";
                result = false;
                return false
            }
            return true;
        }
      };
      //let username = document.getElementById('id_username');
      xhttp.open("GET", "/register/check_username/" + username.value, false);
      xhttp.send();
    }