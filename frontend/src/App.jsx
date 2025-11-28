// import { useState } from "react";
// import "./App.css";
// import Header from "../Components/Header";
// import LQLEditor from "../Components/LqlEditor";
// import OutputPanels from "../Components/OutputPanels";

// export default function App() {
//   const [outputs, setOutputs] = useState({
//     lexerOutput: "",
//     parserOutput: "",
//     semanticAnalyzerOutput: "",
//     intermediateCodeOutput: "",
//     optimizerOutput: "",
//     finalCodeOutput: "",
//   });

//   const [isLoading, setIsLoading] = useState(false);

//   const handleRun = async (code) => {
//     console.log(code);

//     setIsLoading(true);
//     try {
//       const res = await fetch("http://localhost:8000/run", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ code }),
//       });

//       const { phases: data } = await res.json();

//       console.log(data);

//       setOutputs({
//         lexerOutput: JSON.stringify(data.tokens || [], null, 2) || "No output",
//         parserOutput: JSON.stringify(data.parser || [], null, 2) || "No output",
//         semanticAnalyzerOutput:
//           JSON.stringify(data.semantic || {}, null, 2) || "No output",
//         intermediateCodeOutput:
//           JSON.stringify(data.tac || [], null, 2) || "No output",
//         optimizerOutput:
//           JSON.stringify(data.optimized_tac || [], null, 2) || "No output",
//         finalCodeOutput: data.execution_output || "No output",
//       });
//     } catch (err) {
//       const errorMsg = `Error: ${
//         err instanceof Error ? err.message : "Unknown error"
//       }`;
//       setOutputs({
//         lexerOutput: errorMsg,
//         parserOutput: errorMsg,
//         semanticAnalyzerOutput: errorMsg,
//         intermediateCodeOutput: errorMsg,
//         optimizerOutput: errorMsg,
//         finalCodeOutput: errorMsg,
//       });
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   return (
//     <div className="app-container">
//       <Header />
//       <div className="editor-and-outputs">
//         <LQLEditor onRun={handleRun} isLoading={isLoading} />
//         <OutputPanels outputs={outputs} isLoading={isLoading} />
//       </div>
//     </div>
//   );
// }

import { useState } from "react";
import "./App.css";
import Header from "../Components/Header";
import LQLEditor from "../Components/LqlEditor";
import OutputPanels from "../Components/OutputPanels";

export default function App() {
  const [outputs, setOutputs] = useState({
    lexerOutput: "",
    parserOutput: "",
    semanticAnalyzerOutput: "",
    intermediateCodeOutput: "",
    optimizerOutput: "",
    finalCodeOutput: "",
  });

  const [compilerError, setCompilerError] = useState(null);

  const [isLoading, setIsLoading] = useState(false);

  const handleRun = async (code) => {
    setCompilerError(null);
    setIsLoading(true);

    // Start with empty outputs
    let updatedOutputs = {
      lexerOutput: "",
      parserOutput: "",
      semanticAnalyzerOutput: "",
      intermediateCodeOutput: "",
      optimizerOutput: "",
      finalCodeOutput: "",
    };

    try {
      const res = await fetch("http://localhost:8000/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      });

      const result = await res.json();
      const data = result.phases || {};

      // Populate outputs from previous phases
      updatedOutputs.lexerOutput = data.tokens
        ? JSON.stringify(data.tokens, null, 2)
        : "";
      updatedOutputs.parserOutput = data.parser
        ? JSON.stringify(data.parser, null, 2)
        : "";
      updatedOutputs.semanticAnalyzerOutput = data.semantic
        ? JSON.stringify(data.semantic, null, 2)
        : "";
      updatedOutputs.intermediateCodeOutput = data.tac
        ? JSON.stringify(data.tac, null, 2)
        : "";
      updatedOutputs.optimizerOutput = data.optimized_tac
        ? JSON.stringify(data.optimized_tac, null, 2)
        : "";
      updatedOutputs.finalCodeOutput = data.execution_output || "";

      // If an error occurred, show it only in the phase where it happened
      if (!result.success) {
        setCompilerError(`ERROR in ${result.error_phase} PHASE`);

        switch (result.error_phase) {
          case "lexer":
            updatedOutputs.lexerOutput = result.error;
            break;
          case "parser":
            updatedOutputs.parserOutput = result.error;
            break;
          case "semantic":
            updatedOutputs.semanticAnalyzerOutput = result.error;
            break;
          case "tac":
            updatedOutputs.intermediateCodeOutput = result.error;
            break;
          case "optimizer":
            updatedOutputs.optimizerOutput = result.error;
            break;
          case "execution":
            updatedOutputs.finalCodeOutput = result.error;
            break;
          default:
            updatedOutputs.finalCodeOutput = result.error || "Unknown error";
        }
      }

      setOutputs(updatedOutputs);
    } catch (err) {
      const errorMsg = `Error: ${
        err instanceof Error ? err.message : "Unknown error"
      }`;
      setCompilerError(`ERROR in execution PHASE`);
      updatedOutputs.finalCodeOutput = errorMsg;
      setOutputs(updatedOutputs);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <Header />
      <div className="editor-and-outputs">
        <LQLEditor onRun={handleRun} isLoading={isLoading} />
        <OutputPanels
          outputs={outputs}
          isLoading={isLoading}
          compilerError={compilerError}
        />
      </div>
    </div>
  );
}
