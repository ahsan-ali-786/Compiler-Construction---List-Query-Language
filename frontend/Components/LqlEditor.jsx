import { useState } from "react";
import Editor from "@monaco-editor/react";

const customSyntaxHighlighter = (monaco) => {
  // 1. Register the language
  monaco.languages.register({ id: "lql" });

  // 2. Tokenizer rules
  monaco.languages.setMonarchTokensProvider("lql", {
    keywords: [
      "list",
      "filter",
      "sort",
      "asc",
      "desc",
      "map",
      "print",
      "mean",
      "sum",
      "median",
      "variance",
      "std",
      "min",
      "max",
      "count",
      "union",
      "intersection",
      "difference",
    ],

    operators: [
      "=",
      ">=",
      "<=",
      ">",
      "<",
      "==",
      "+",
      "-",
      "*",
      "/",
      "=>",
      "and",
      "or",
      "xor",
    ],

    tokenizer: {
      root: [
        // --- Comments starting with @ till end of line ---
        [/@.*$/, "comment"],

        // --- Keywords ---
        [
          /\b(list|filter|sort|asc|desc|map|print|mean|sum|median|variance|std|min|max|count|union|intersection|difference)\b/,
          "keyword",
        ],

        // --- Logical operators ---
        [/\b(and|or|xor)\b/, "operator"],

        // --- Numbers ---
        [/\b\d+(\.\d+)?\b/, "number"],

        // --- Operators ---
        [/(>=|<=|==|=>|\+|-|\*|\/|=|>|<|%)/, "operator"],

        // --- Identifiers ---
        [/[a-zA-Z_][a-zA-Z0-9_]*/, "identifier"],

        // --- Brackets ---
        [/\[|\]/, "delimiter.square"],
        [/\(|\)/, "delimiter.parenthesis"],
        [/\{|\}/, "delimiter.brace"],

        // --- Whitespace ---
        [/\s+/, "white"],
      ],
    },
  });

  // 3. Theme
  monaco.editor.defineTheme("lql-dark", {
    base: "vs-dark",
    inherit: true,
    rules: [
      { token: "keyword", foreground: "FFB000", fontStyle: "bold" },
      { token: "number", foreground: "61AFEF" },
      { token: "operator", foreground: "56B6C2" },
      { token: "identifier", foreground: "E5C07B" },
      { token: "delimiter.square", foreground: "C678DD" },
      { token: "comment", foreground: "7F848E", fontStyle: "italic" }, // comments
    ],
    colors: {},
  });
};

export default function LQLEditor({ onRun, isLoading }) {
  const [code, setCode] = useState(`@ Example Code:\nlist data = [1, 2, 3, 4, 5]
list big = filter data >= 3
list sq = map data $0 => $0 * $0
print sq
print mean sq
list l1 = [2,4,5,6]
list l2 = [3,3]
list res = l1 union l2 union [0,9,8,7]
print res`);

  const handleRun = () => onRun(code);

  return (
    <div className="editor-panel">
      <div className="editor-header">
        <span className="editor-title">Code Editor</span>
      </div>

      <Editor
        height="100%"
        width="100%"
        value={code}
        theme="lql-dark"
        language="lql"
        onChange={(v) => setCode(v || "")}
        beforeMount={(monaco) => customSyntaxHighlighter(monaco)}
        options={{
          fontSize: 14,
          minimap: { enabled: false },
          scrollBeyondLastLine: false,
          wordWrap: "on",
          padding: { top: 12, bottom: 12 },
          lineNumbersMinChars: 3,
        }}
      />

      <button onClick={handleRun} disabled={isLoading} className="run-button">
        {isLoading ? "Running..." : "▶ Run Code"}
      </button>
    </div>
  );
}
