/**************************************
    File Name: custom.js
    Template Name: Linux Users Group
    Created By: hbsoft 
    http://hbsoft.ir
**************************************/

(function ($) {
    "use strict";
    $(document).ready(function () {
        $('#nav-expander').on('click', function (e) {
            e.preventDefault();
            $('body').toggleClass('nav-expanded');
        });
        $('#nav-close').on('click', function (e) {
            e.preventDefault();
            $('body').removeClass('nav-expanded');
        });
    });

    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    })

    $('.carousel').carousel({
        interval: 4000
    })

    $(window).load(function () {
        $("#preloader").on(500).fadeOut();
        $(".preloader").on(600).fadeOut("slow");
    });

    jQuery(window).scroll(function () {
        if (jQuery(this).scrollTop() > 1) {
            jQuery('.dmtop').css({ bottom: "25px" });
        } else {
            jQuery('.dmtop').css({ bottom: "-100px" });
        }
    });
    jQuery('.dmtop').click(function () {
        jQuery('html, body').animate({ scrollTop: '0px' }, 800);
        return false;
    });

})(jQuery);


function openCategory(evt, catName) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the link that opened the tab
    document.getElementById(catName).style.display = "block";
    evt.currentTarget.className += " active";
}

$(function () {

    var $formLogin = $('#login-form');
    var $formLost = $('#lost-form');
    var $formRegister = $('#register-form');
    var $divForms = $('#div-forms');
    var $modalAnimateTime = 300;
    var $msgAnimateTime = 150;
    var $msgShowTime = 2000;

    function password_check(){
        var pass1 = $("#register_password").val();
        var pass2 = $("#register_password_confirm").val();
        if (pass1 != pass2){
            $('#incorrect-pass').value = "پسوورد ها مطابقات ندارند";
            $('#incorrect-pass').css('display', 'block');
        }else{
            $('#incorrect-pass').css('display', 'none');
        }
    }

    // $('#register_password').on("change", function(){
    //     password_check();
    // });

    // $('#register_password_confirm').on("change", function(){
    //     password_check();
    // });

    $("form").submit(function () {
        switch (this.id) {
            case "login-form":
                var $lg_username = $('#login_username').val();
                var $lg_password = $('#login_password').val();
                if ($lg_username == "ERROR") {
                    msgChange($('#div-login-msg'), $('#icon-login-msg'), $('#text-login-msg'), "error", "glyphicon-remove", "لطفا تمام فید ها را تکمیل کنید");
                } else {
                    $.ajax({
                        type: "POST",
                        url:"/login",
                        data: { 
                            username:$("#login_username").val(),
                            password:$("#login_password").val(),
                            csrfmiddlewaretoken : $("input[name='csrfmiddlewaretoken']").val(),
                        },
                            success:function(response){
                                switch(response){
                                    case 'ok':
                                        msgChange($('#div-login-msg'), $('#icon-login-msg'), $('#text-login-msg'), "success", "glyphicon-ok", "با موفقیت وارد سیستم شدید");
                                        setTimeout(function(){ location.reload(); }, 1000);
                                        
                                        break;
                                    case 'wrong':
                                        msgChange($('#div-login-msg'), $('#icon-login-msg'), $('#text-login-msg'), "error", "glyphicon-remove", "نام کاربری یا رمز عبور نادرست است");
                                        break;
                                    default:
                                        msgChange($('#div-login-msg'), $('#icon-login-msg'), $('#text-login-msg'), "error", "glyphicon-remove", "خطایی غیرمنتظره رخ داد");
                                        
                                }
                            },
                        error:function (){
                            msgChange($('#div-login-msg'), $('#icon-login-msg'), $('#text-login-msg'), "error", "glyphicon-remove", "خطایی غیرمنتظره رخ داد");

                        }
                    });
                }

                return false;
                break;
            case 'form-user':
                return true;
            case "lost-form":
                msgChange($('#div-lost-msg'), $('#icon-lost-msg'), $('#text-lost-msg'), "success", "glyphicon-ok", "لطفا صبر کنید", true);
                
                $.when(reset_password()).done(function(){
                    return false;
                });
                break;

            case "register-form":
                var $rg_username = $('#register_username').val();
                var $rg_email = $('#register_email').val();
                var $rg_password = $('#register_password').val();
                var $rg_password2 = $('#register_password_confirm').val();
                var $rg_first_name = $("#register_first_name").val();
                var $rg_last_name = $("#register_last_name").val();
                var $rg_expertise = $("#register_expertise").val();
                

                if ($rg_username == "ERROR") {
                    msgChange($('#div-register-msg'), $('#icon-register-msg'), $('#text-register-msg'), "error", "glyphicon-remove", "خطایی رخ داد");
                    return false;
                } else {
                    $.ajax({
                        type: "POST",
                        url: "/register",
                        data: {
                            email: $rg_email,
                            username: $rg_username,
                            password1: $rg_password,
                            password2: $rg_password2,
                            first_name: $rg_first_name,
                            last_name: $rg_last_name,
                            expertise: $rg_expertise,
                            csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
                        },
                        success:function(response){
                            if(response=="success"){
                                msgChange($('#div-register-msg'), $('#icon-register-msg'), $('#text-register-msg'), "success", "glyphicon-ok", "حساب با موفقیت ساخته شد");
                                modalAnimate($formRegister, $formLogin);
                                return false;
                            }
                            msgChange($('#div-register-msg'), $('#icon-register-msg'), $('#text-register-msg'), "error", "glyphicon-remove", response);
                            return false;
                        }
                    });
                    return false;
                }
                break;

            default:
                return true;
        }
        return false;
    });

    $('#login_register_btn').click(function () { modalAnimate($formLogin, $formRegister) });
    $('#register_login_btn').click(function () { modalAnimate($formRegister, $formLogin); });
    $('#login_lost_btn').click(function () { modalAnimate($formLogin, $formLost); });
    $('#lost_login_btn').click(function () { modalAnimate($formLost, $formLogin); });
    $('#lost_register_btn').click(function () { modalAnimate($formLost, $formRegister); });
    $('#register_lost_btn').click(function () { modalAnimate($formRegister, $formLost); });

    function modalAnimate($oldForm, $newForm) {
        var $oldH = $oldForm.height();
        var $newH = $newForm.height();
        $divForms.css("height", $oldH);
        $oldForm.fadeToggle($modalAnimateTime, function () {
            $divForms.animate({ height: $newH }, $modalAnimateTime, function () {
                $newForm.fadeToggle($modalAnimateTime);
            });
        });
    }

    function msgFade($msgId, $msgText) {
        $msgId.fadeOut($msgAnimateTime, function () {
            $(this).text($msgText).fadeIn($msgAnimateTime);
        });
    }

    function msgChange($divTag, $iconTag, $textTag, $divClass, $iconClass, $msgText, $showtime=false) {
        var $msgOld = $divTag.text();
        msgFade($textTag, $msgText);
        $divTag.addClass($divClass);
        $iconTag.removeClass("glyphicon-chevron-right");
        $iconTag.addClass($iconClass + " " + $divClass);
        $iconTag.removeClass($iconClass + " " + $divClass);
        if (!$showtime){
            setTimeout(function () {
                msgFade($textTag, $msgOld);
                $divTag.removeClass($divClass);
                $iconTag.addClass("glyphicon-chevron-right");
            }, $msgShowTime);
        }
    }
    function reset_password(){
        var $ls_email = $('#lost_email').val();
        var csrf = $("input[name='csrfmiddlewaretoken']").val();
        if ($ls_email == "ERROR") {
        } else {
            $.ajax({
                type: "POST",
                url: "/reset-password",
                data: {
                    "email": $('#lost_email').val(),
                    "csrfmiddlewaretoken": csrf,
                    "recaptcha": $("#g-recaptcha-response").val()
                },
                success: function(){
                    msgChange($('#div-lost-msg'), $('#icon-lost-msg'), $('#text-lost-msg'), "success", "glyphicon-ok", "ایمیل بازیابی با موفقیت ارسال شد");
                    setTimeout(function (){
                        modalAnimate($formLost, $formLogin);
                    }, 2000);
                },
                error: function(){
                    msgChange($('#div-lost-msg'), $('#icon-lost-msg'), $('#text-lost-msg'), "error", "glyphicon-remove", "خطایی رخ داد مجددا تلاش فرمایید", true);
                }
            });
        }
        return false;
    }
});
grecaptcha.ready(function() {
    // do request for recaptcha token
    // response is promise with passed token
    grecaptcha.execute($("#sitekey").val(), {action:'validate_captcha'}).then(function(token) {
            // add token value to form
        document.getElementById('g-recaptcha-response').value = token;
    });
});