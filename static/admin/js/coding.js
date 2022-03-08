function djangocodemirror() {
    const textarea = document.querySelector("textarea");

    textarea.addEventListener("keydown", (e) => {
        if (e.keyCode == 9) {
            e.preventDefault();

            var stmt_list = textarea.value.substr(0, textarea.selectionStart).split("\n");
            var cusor_stmt = stmt_list[stmt_list.length - 1];
            var found = cusor_stmt.match(/\S+/);
            if (found == null) {
                indent = cusor_stmt.length;
            }
            else {
                indent = found?.index;
            }

            tabSize = 4 - (indent % 4);

            if (tabSize == 4) {
                tab = "    ";
            }
            else if (tabSize == 3) {
                tab = "   ";
            }
            else if (tabSize == 2) {
                tab = "  ";
            }
            else {
                tab = " ";
            }

            textarea.setRangeText(
                tab,
                textarea.selectionStart,
                textarea.selectionStart,
                "end"
            );
        }
    });
}