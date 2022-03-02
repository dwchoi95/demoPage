function copyClipboard(text) {
    const ta = document.createElement('textarea');
    ta.textContent = "print("+text+")";
    document.body.append(ta);
    ta.select();
    document.execCommand('copy');
    ta.remove();
}