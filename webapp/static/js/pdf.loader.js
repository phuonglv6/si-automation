var doc_path = $("#doc_path").text()
renderPDF('/static/media/' + doc_path + '/', document.getElementById('holder'));
function renderPDF(url, canvasContainer, options) {
var options = options || { scale: 1.5 };
function renderPage(page) {
    var viewport = page.getViewport(options.scale);
    var canvas = document.createElement('canvas');
    var ctx = canvas.getContext('2d');
    var renderContext = {
    canvasContext: ctx,
    viewport: viewport
    };
    canvas.height = viewport.height;
    canvas.width = viewport.width;
    canvasContainer.appendChild(canvas);
    page.render(renderContext);
}

function renderPages(pdfDoc) {
    for(var num = 1; num <= pdfDoc.numPages; num++)
        pdfDoc.getPage(num).then(renderPage);
}
// PDFJS.disableWorker = true;
PDFJS.getDocument(url).then(renderPages);
} 