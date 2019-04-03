    function validateMyForm() {
        let staff_id = document.getElementById('staff_id');
        let str_staff_id = staff_id.value + "";
        if (str_staff_id.length < 8) {
            let message = document.getElementById('message');
            message.innerHTML = "<p>The length of the Staff ID must be 8 digit</p>";
            return false;
        } else
            return true;

    }