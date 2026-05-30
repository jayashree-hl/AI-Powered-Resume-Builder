// =========================
// AI Resume Builder Script
// =========================

console.log("AI Resume Builder Loaded Successfully");

// =========================
// FORM VALIDATION
// =========================

document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector("form");

    if(form){

        form.addEventListener("submit", (e) => {

            const name = document.querySelector("input[name='name']");
            const email = document.querySelector("input[name='email']");
            const phone = document.querySelector("input[name='phone']");

            // NAME VALIDATION
            if(name && name.value.trim().length < 3){

                alert("Name must contain at least 3 characters");
                e.preventDefault();
                return;
            }

            // EMAIL VALIDATION
            if(email){

                const emailPattern =
                    /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;

                if(!email.value.match(emailPattern)){

                    alert("Enter a valid email address");
                    e.preventDefault();
                    return;
                }
            }

            // PHONE VALIDATION
            if(phone){

                const phonePattern = /^[0-9]{10}$/;

                if(!phone.value.match(phonePattern)){

                    alert("Phone number must contain 10 digits");
                    e.preventDefault();
                    return;
                }
            }

        });

    }

});

// =========================
// PASSWORD SHOW/HIDE
// =========================

const passwordField =
    document.querySelector("input[type='password']");

if(passwordField){

    const toggleBtn = document.createElement("span");

    toggleBtn.innerHTML =
        '<i class="fa-solid fa-eye"></i>';

    toggleBtn.style.position = "absolute";
    toggleBtn.style.right = "15px";
    toggleBtn.style.top = "15px";
    toggleBtn.style.cursor = "pointer";
    toggleBtn.style.color = "#777";

    passwordField.parentElement.appendChild(toggleBtn);

    toggleBtn.addEventListener("click", () => {

        if(passwordField.type === "password"){

            passwordField.type = "text";

            toggleBtn.innerHTML =
                '<i class="fa-solid fa-eye-slash"></i>';

        }else{

            passwordField.type = "password";

            toggleBtn.innerHTML =
                '<i class="fa-solid fa-eye"></i>';
        }

    });

}

// =========================
// SMOOTH ANIMATION
// =========================

window.addEventListener("load", () => {

    document.body.style.opacity = "1";

});

// =========================
// SUCCESS MESSAGE
// =========================

function showSuccessMessage(message){

    const successDiv = document.createElement("div");

    successDiv.innerText = message;

    successDiv.style.position = "fixed";
    successDiv.style.top = "20px";
    successDiv.style.right = "20px";
    successDiv.style.background = "#28a745";
    successDiv.style.color = "white";
    successDiv.style.padding = "15px 20px";
    successDiv.style.borderRadius = "10px";
    successDiv.style.boxShadow =
        "0 5px 10px rgba(0,0,0,0.2)";
    successDiv.style.zIndex = "999";

    document.body.appendChild(successDiv);

    setTimeout(() => {

        successDiv.remove();

    }, 3000);

}

// =========================
// BUTTON HOVER EFFECT
// =========================

const buttons = document.querySelectorAll("button");

buttons.forEach((btn) => {

    btn.addEventListener("mouseover", () => {

        btn.style.transform = "scale(1.02)";

    });

    btn.addEventListener("mouseout", () => {

        btn.style.transform = "scale(1)";
    });

});

// =========================
// RESUME DOWNLOAD ALERT
// =========================

const downloadBtn =
    document.querySelector(".download-btn");

if(downloadBtn){

    downloadBtn.addEventListener("click", () => {

        showSuccessMessage(
            "Resume PDF Download Started!"
        );

    });

}

// =========================
// TYPING EFFECT
// =========================

const subtitle =
    document.querySelector(".subtitle");

if(subtitle){

    const text = subtitle.innerText;

    subtitle.innerText = "";

    let i = 0;

    function typingEffect(){

        if(i < text.length){

            subtitle.innerText += text.charAt(i);

            i++;

            setTimeout(typingEffect, 40);
        }
    }

    typingEffect();

}

// =========================
// DARK MODE TOGGLE
// =========================

const darkModeBtn =
    document.createElement("button");

darkModeBtn.innerHTML =
    '<i class="fa-solid fa-moon"></i>';

darkModeBtn.style.position = "fixed";
darkModeBtn.style.bottom = "20px";
darkModeBtn.style.right = "20px";
darkModeBtn.style.width = "55px";
darkModeBtn.style.height = "55px";
darkModeBtn.style.borderRadius = "50%";
darkModeBtn.style.border = "none";
darkModeBtn.style.background = "#222";
darkModeBtn.style.color = "white";
darkModeBtn.style.cursor = "pointer";
darkModeBtn.style.zIndex = "999";

document.body.appendChild(darkModeBtn);

let darkMode = false;

darkModeBtn.addEventListener("click", () => {

    darkMode = !darkMode;

    if(darkMode){

        document.body.style.background =
            "#121212";

        document.body.style.color =
            "white";

        darkModeBtn.innerHTML =
            '<i class="fa-solid fa-sun"></i>';

    }else{

        document.body.style.background =
            "linear-gradient(135deg,#4facfe,#00f2fe)";

        document.body.style.color =
            "#333";

        darkModeBtn.innerHTML =
            '<i class="fa-solid fa-moon"></i>';
    }

});

// =========================
// END
// =========================