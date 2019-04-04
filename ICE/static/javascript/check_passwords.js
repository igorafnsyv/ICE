    function checkPassword(){
        let username = document.getElementById('username');
        let password1 = document.getElementById('password1');
        let password2 = document.getElementById('password2');

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

        return true;

    }