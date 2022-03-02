document.addEventListener('DOMContentLoaded', function () {
    const diffString = document.getElementById('diff2str').value;
    var targetElement = document.getElementById('myDiffElement');
    var configuration = {
    drawFileList: false,
    fileListToggle: false,
    fileListStartVisible: false,
    fileContentToggle: false,
    matching: 'lines',
    outputFormat: 'line-by-line',
    synchronisedScroll: true,
    highlight: true,
    renderNothingWhenEmpty: false
    };
    var diff2htmlUi = new Diff2HtmlUI(targetElement, diffString, configuration);
    diff2htmlUi.draw();
    diff2htmlUi.highlightCode();
});