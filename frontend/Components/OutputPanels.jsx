import OutputCard from "./OutputCard";

export default function OutputPanels({
  outputs,
  isLoading,
  compilerError = null,
}) {
  const panels = [
    {
      id: "lexer",
      title: "Lexer Output",
      icon: "🔤",
      content: outputs.lexerOutput,
      description: "Tokenization results",
    },
    {
      id: "parser",
      title: "Parser Output",
      icon: "🌳",
      content: outputs.parserOutput,
      description: "Abstract Syntax Tree",
    },
    {
      id: "semantic",
      title: "Semantic Analyzer",
      icon: "✓",
      content: outputs.semanticAnalyzerOutput,
      description: "Type checking & validation",
    },
    {
      id: "intermediate",
      title: "Intermediate Code",
      icon: "⚙",
      content: outputs.intermediateCodeOutput,
      description: "TAC representation",
    },
    {
      id: "optimizer",
      title: "Optimizer Output",
      icon: "⚡",
      content: outputs.optimizerOutput,
      description: "Optimized instructions",
    },
    {
      id: "final",
      title: "Final Code Output",
      icon: "📤",
      content: outputs.finalCodeOutput,
      description: "Compiled result",
    },
  ];

  return (
    <div className="outputs-panel">
      <div className="outputs-header">
        <span className="outputs-title">
          Compilation Pipeline{" "}
          {compilerError && <span className="error"> {compilerError} </span>}
        </span>
        {isLoading && <span className="loading-indicator">● Compiling...</span>}
      </div>
      <div className="outputs-grid">
        {panels.map((panel) => (
          <OutputCard key={panel.id} panel={panel} />
        ))}
      </div>
    </div>
  );
}
