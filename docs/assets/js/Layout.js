//function hexToRGB(h) {
//    let r = 0, g = 0, b = 0;
//    // 3 digits
//    if (h.length == 4) {
//        r = "0x" + h[1] + h[1];
//        g = "0x" + h[2] + h[2];
//        b = "0x" + h[3] + h[3];
//    // 6 digits
//    } else if (h.length == 7) {
//        r = "0x" + h[1] + h[2];
//        g = "0x" + h[3] + h[4];
//        b = "0x" + h[5] + h[6];
//    }
//    return "rgb("+ +r + "," + +g + "," + +b + ")";
//}
//$(function () {
var maincolor = $('body').data('maincolor');
//var navBGA = hexToRGB(maincolor);
var navBG = maincolor;

var subcolor = $('body').data('subcolor');
//var footerBG = hexToRGB(subcolor);
var footerBG = subcolor;

var SwitchColor = $('body').data('switchcolor');

var Opacity = $('body').data('opacity');
var FixedTop = $('body').data('fixedtop');
var HeaderBlock = $('body').data('headerblock');
var NavStyle = $('body').data('navstyle');

$('footer').css("background-color", footerBG);
$('img').not('.img-fluid').not('.gg-box img').addClass('img-fluid');

function getcontrast(hex) {
    let r = parseInt(hex.substr(1, 2), 16),
        g = parseInt(hex.substr(3, 2), 16),
        b = parseInt(hex.substr(5, 2), 16),
        yiq = ((r * 299) + (g * 587) + (b * 114)) / 1000;
    return (yiq >= 128) ? '#000000' : '#ffffff';
}
//});
// var LayoutApp = (function () {
//     var _private = {
//         navBG: "",
//         footerBG: "",
//         SwitchColor: "",
//         Opacity: "",
//         FixedTop: "",
//         HeaderBlock: "",
//         NavStyle: "",
//         init: function (_body) {
//             this.navBG = _body.data('maincolor');
//             this.footerBG = _body.data('subcolor');
//             this.SwitchColor = _body.data('switchcolor');
//             this.Opacity = _body.data('opacity');
//             this.FixedTop = _body.data('fixedtop');
//             this.HeaderBlock = _body.data('headerblock');
//             this.NavStyle = _body.data('navstyle');

//             let Footer = $('footer');
//             Footer.css("background-color", this.footerBG);
//             $('img').not('.img-fluid').not('.gg-box img').addClass('img-fluid');

//         },
//     };
//     return {
//         init: function (_body) {
//             _private.init(_body);
//         },

//     }
// }())
// $(function () {
//     LayoutApp.init($('body'));
// })