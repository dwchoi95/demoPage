function copyClipboard(in_tc, out_tc) {
    const ta = document.createElement('textarea');
    ta.textContent = "print(" + in_tc + " == " + out_tc + ")";
    document.body.append(ta);
    ta.select();
    document.execCommand('copy');
    ta.remove();
}