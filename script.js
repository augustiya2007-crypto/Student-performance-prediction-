// Delete Confirmation

function confirmDelete(){

    let answer = confirm(
        "Are you sure you want to delete this student?"
    );

    return answer;

}



// Input Validation

function validateInput(){

    let study = document.getElementById("study").value;

    let attendance = document.getElementById("attendance").value;

    let internal = document.getElementById("internal").value;

    let assignment = document.getElementById("assignment").value;



    if(
        study < 0 ||
        attendance < 0 ||
        internal < 0 ||
        assignment < 0
    ){

        alert("Please enter valid values");

        return false;

    }


    if(
        attendance > 100 ||
        internal > 100 ||
        assignment > 100
    ){

        alert("Marks and attendance cannot exceed 100");

        return false;

    }


    return true;

}



// Login Alert

function loginSuccess(){

    alert("Login Successful");

}



// Register Alert

function registerSuccess(){

    alert("Registration Successful");

}