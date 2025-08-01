let teach_log_form = document.querySelector('#teach-log');
let stu_log_form = document.querySelector('#stu-log');
let stu_reg_form = document.querySelector('#stu-reg');
let teach_reg_form = document.querySelector('#teach-reg');
let form_detail = document.querySelector('#form-detail');
let stu_img = document.querySelector('#stu-img');
let teach_img = document.querySelector('#teach-img');
let role_teach = document.querySelector('#role-ch2');
let role_stu = document.querySelector('#role-ch3');



function teach_log()
{
    teach_log_form.style.display = 'block';
    teach_reg_form.style.display = 'none';
    stu_reg_form.style.display = 'none';
    stu_log_form.style.display = 'none';
    form_detail.style.height = '60%';

    teach_img.style.border = '3px solid black';
    stu_img.style.border = '1px solid black';
    role_teach.style.color = 'black';
    role_stu.style.color = 'rgba(0, 0, 0, 0.5)';
}

function stu_log()
{
    teach_log_form.style.display = 'none';
    teach_reg_form.style.display = 'none';
    stu_reg_form.style.display = 'none';
    stu_log_form.style.display = 'block';
    form_detail.style.height = '60%';

    stu_img.style.border = '3px solid black';
    teach_img.style.border = '1px solid black';
    role_teach.style.color = 'rgba(0, 0, 0, 0.5)';
    role_stu.style.color = 'black';
}

function show_stu_reg()
{
    teach_log_form.style.display = 'none';
    teach_reg_form.style.display = 'none';
    stu_reg_form.style.display = 'block';
    stu_log_form.style.display = 'none';
    form_detail.style.height = '95%';
}

function show_teach_reg()
{
    teach_log_form.style.display = 'none';
    teach_reg_form.style.display = 'block';
    stu_reg_form.style.display = 'none';
    stu_log_form.style.display = 'none';
    form_detail.style.height = '80%';
}

function show_slide(){
    let sidebar = document.querySelector('.side-bar');

    sidebar.style.display = 'flex';
}

function hide_slide(){
    let sidebar = document.querySelector('.side-bar');

    sidebar.style.display = 'none';
}

function checkFileSize() {
    var input = document.getElementById("photo");
    var fileSizeMsg = document.getElementById("fileSizeMsg");
    if ('files' in input && input.files.length > 0) {
        var fileSize = input.files[0].size / 1024 / 1024; // size in MB
        if (fileSize > 5) {
            fileSizeMsg.textContent = "File size must not exceed 5 MB.";
            fileSizeMsg.style.color = "red";
            return false;
        } else {
            fileSizeMsg.textContent = "";
        }
    }
    return true;
}


function checkFileSize1() {
    var input = document.getElementById("upload-img");
    var fileSizeMsg = document.getElementById("fileSizeMsg");
    if ('files' in input && input.files.length > 0) {
        var fileSize = input.files[0].size / 1024 / 1024; // size in MB
        if (fileSize > 10) {
            fileSizeMsg.textContent = "File size must not exceed 10 MB.";
            fileSizeMsg.style.color = "red";
            return false;
        } else {
            fileSizeMsg.textContent = "";
        }
    }
    return true;
}

document.addEventListener("DOMContentLoaded", function() {
    const textContainer = document.getElementById("main-co-container");
    const text = "Effortlessly capture classroom moments, recognize faces, and mark attendance seamlessly..."; // Replace with your text
    let i = 0;

    function typeWriter() {
        if (i < text.length) {
            textContainer.innerHTML += text.charAt(i);
            i++;
            setTimeout(typeWriter, 100); // Adjust typing speed
        }
    }

    typeWriter();
});
