/* 用export把方法暴露出来 */
/* 设置cookie */
export function setCookie(name, value) {
  var str = name+ '=' + value; //eslint-disable-line
  var date = new Date(); //eslint-disable-line
  var ms = 1 * 3600 * 1000*24; //eslint-disable-line
  date.setTime(date.getTime() + ms);
  str += "; expires=" + date.toGMTString(); //eslint-disable-line
  document.cookie = str;
}

/* 获取cookie */
export function getCookie(cname) {
  var name = cname + "="; //eslint-disable-line
  var ca = document.cookie.split(';'); //eslint-disable-line
  for (var i = 0; i < ca.length; i++) { //eslint-disable-line
    var c = ca[i]; //eslint-disable-line
    if (c.indexOf('uid') != -1) continue;
    while (c.charAt(0) == ' ') c = c.substring(1); //eslint-disable-line
    if (c.indexOf(name) != -1){ //eslint-disable-line
      if (name !== 'id=') {
        return c.substring(name.length, c.length);
      } else if (c.indexOf('id="') === -1) {
        return c.substring(name.length, c.length);
      }
    }
  }
  return '';
}

/* 删除cookie */
export function delCookie(name) {
  setCookie(name, '', -1);
}
