import html2Canvas from 'html2canvas'
import JsPDF from 'jspdf'
import $ from 'jquery'

export default{
    install: function (Vue, options) {
      Vue.prototype.getPdf = function (dom,title) {
          var title = title;
          var c = document.createElement("canvas");
          // c.width = $(dom).width() * 2;
          // c.height = $(dom).height() * 2;
          c.width = $(dom).outerWidth() * 2;
          c.height = $(dom).outerHeight() * 2;
          c.getContext("2d").scale(2, 2);
          var opts = {
            scale: 2,
            canvas: c,
            logging: false,
            allowTaint: false,
            useCORS: true,
            tainttest: false,
            dpi: 72,
          };
          html2Canvas(document.querySelector(dom), opts).then(function (canvas) {
              // var imgUri = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream"); // 获取生成的图片的url  
              // window.location.href= imgUri;
              var contentWidth = canvas.width;
              var contentHeight = canvas.height;
              var pageHeight = contentWidth / 592.28 * 841.89;
              var leftHeight = contentHeight;
              var position = 0;
              var imgWidth = 592.28;
              var imgHeight = 592.28 / contentWidth * contentHeight;
              var pageData = canvas.toDataURL('image/jpeg', 1.0);
              var PDF = new JsPDF('', 'pt', 'a4');
              if (leftHeight < pageHeight) {
                  PDF.addImage(pageData, 'JPEG', 0, 0, imgWidth, imgHeight);
              } else {
                  while (leftHeight > 0) {
                      PDF.addImage(pageData, 'JPEG', 0, position, imgWidth, imgHeight);
                      leftHeight -= pageHeight;
                      position -= 841.89;
                      if (leftHeight > 0) {
                          PDF.addPage();
                      }
                    }
                }
              PDF.save(title + '.pdf');
            }
          );
        }
    }
}
