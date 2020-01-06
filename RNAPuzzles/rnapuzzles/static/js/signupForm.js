document.getElementById("id_role").onchange =  function(){
    if(document.getElementById("id_role").value == "1"){        //organizer
        console.log('organizer');
        (document.getElementById("id_institution")).setAttribute('type', 'hidden');
        (document.getElementById("div_id_institution")).style.display = "none";
        (document.getElementById("id_group_name")).setAttribute('type', 'hidden');
        (document.getElementById("div_id_group_name")).style.display = "none";
        (document.getElementById("id_new_group_name")).setAttribute('type', 'hidden');
        (document.getElementById("div_id_new_group_name")).style.display = "none";
        }
    else if(document.getElementById("id_role").value == "2"){          //participant
        console.log('participant');
        (document.getElementById("id_institution")).setAttribute('type', '');
        (document.getElementById("div_id_institution")).style.display = "block";
        (document.getElementById("id_group_name")).setAttribute('type', '');
        (document.getElementById("div_id_group_name")).style.display = "block";
        (document.getElementById("id_new_group_name")).setAttribute('type', 'hidden');
        (document.getElementById("div_id_new_group_name")).style.display = "none";

    }
    else if(document.getElementById("id_role").value == "3"){            //group leader
        (document.getElementById("id_institution")).setAttribute('type', '');
        (document.getElementById("div_id_institution")).style.display = "block";
        (document.getElementById("id_group_name")).setAttribute('type', 'hidden');
        (document.getElementById("div_id_group_name")).style.display = "none";
        (document.getElementById("id_new_group_name")).setAttribute('type', '');
        (document.getElementById("div_id_new_group_name")).style.display = "block";
    }
};

        (document.getElementById("id_institution")).setAttribute('type', 'hidden');
        (document.getElementById("div_id_institution")).style.display = "none";
        (document.getElementById("id_group_name")).setAttribute('type', 'hidden');
        (document.getElementById("div_id_group_name")).style.display = "none";
        (document.getElementById("id_new_group_name")).setAttribute('type', 'hidden');
        (document.getElementById("div_id_new_group_name")).style.display = "none";